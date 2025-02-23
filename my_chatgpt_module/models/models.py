from odoo import models, fields, api
import json
import re
from openai import OpenAI
import time
from dotenv import load_dotenv
import os


load_dotenv()

class ChatGPTModule(models.Model):
    _name = 'chatgpt.module'
    _description = 'ChatGPT Integration'

    question = fields.Text(string="Question", required=True)
    answer = fields.Text(string="Answer", readonly=True)

    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def clean_code_response(self, raw_response):
        cleaned = re.sub(r"```[\w]*", "", raw_response, flags=re.MULTILINE)
        cleaned = cleaned.replace("```", "").strip()
        print("Cleaned response:", cleaned)
        return cleaned

    def clean_model_name(self, model_name):
        cleaned_model = re.sub(r"[^\w.]", "", model_name).strip()
        print("Cleaned model name:", cleaned_model)
        return cleaned_model

    def get_valid_model(self, model_name):
        model_record = self.env['ir.model'].search([('model', '=', model_name)], limit=1)
        valid_model = model_record.model if model_record else None
        print("Valid model from DB:", valid_model)
        return valid_model

    def get_valid_fields(self, model_name):
        fields_rec = self.env['ir.model.fields'].search([
            ('model', '=', model_name),
            ('store', '=', True),
            ('ttype', 'not in', ('one2many', 'many2many'))
        ])
        valid_fields = [field.name for field in fields_rec] if fields_rec else []
        print(f"Available (stored) fields for model {model_name}:", valid_fields)
        return valid_fields

    def get_available_models(self):
        models_rec = self.env['ir.model'].search([])
        available_models = [rec.model for rec in models_rec]
        print("Available models in system:", available_models)
        return available_models

    def get_manual_search_instructions(self, model, question):
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an AI assistant specialized in Odoo. "
                            "Provide a concise, step-by-step guide in table format to help the user manually locate the required information in the Odoo UI."
                        )
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Question: '{question}'\nModel: '{model}'\n"
                            "No results were found from the query. Please provide a clear step-by-step manual guide (preferably in table format) "
                            "to help the user locate this information in the Odoo interface."
                        )
                    }
                ]
            )
            manual_instructions = response.choices[0].message.content.strip()
            print("Manual search instructions:", manual_instructions)
            return manual_instructions
        except Exception as e:
            print(f"Error generating manual search instructions: {e}")
            return (
                " لم يتم العثور على نتائج.\n\n"
                "يرجى اتباع الخطوات التالية يدويًا:\n"
                "1. انتقل إلى الموديل المناسب عبر قائمة التطبيقات.\n"
                "2. استخدم شريط البحث لإدخال المعايير المطلوبة.\n"
                "3. تأكد من تحديد الفلاتر الصحيحة لمطابقة البيانات المطلوبة.\n"
                "4. إذا استمرت المشكلة، راجع إعدادات البحث أو استشر المسؤول."
            )

    def generate_model_fields_and_domain_query(self, question):
        print("\n--- Starting generate_model_fields_and_domain_query ---")
        available_models = self.get_available_models()

        try:
            print("Generating model based on question...")
            model_response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an AI assistant specialized in the Odoo system. "
                            "Determine the correct Odoo model based on the user's question and the provided list of available models. "
                            "Return only the model name without any explanation."
                        )
                    },
                    {
                        "role": "user",
                        "content": f"Question: '{question}'\nAvailable models: {available_models}"
                    }
                ]
            )
            raw_model = model_response.choices[0].message.content.strip()
            print("Raw model response:", raw_model)
            model = self.clean_model_name(raw_model)
            valid_model = self.get_valid_model(model)
            if not valid_model:
                print("Model not valid. Using default 'res.partner'")
                valid_model = 'res.partner'
        except Exception as e:
            print(f"Error generating model: {e}")
            valid_model = 'res.partner'

        available_fields = self.get_valid_fields(valid_model)

        try:
            print("Generating relevant fields based on question and model...")
            fields_response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an AI assistant specialized in Odoo. "
                            "Based on the user's question, the chosen model, and the available fields, "
                            "return a JSON array of field names that are most relevant for the query. "
                            "Ensure the field names exactly match those in Odoo and provide only a JSON array."
                        )
                    },
                    {
                        "role": "user",
                        "content": f"Question: '{question}'\nModel: '{valid_model}'\nAvailable fields: {available_fields}"
                    }
                ]
            )
            raw_fields = fields_response.choices[0].message.content.strip()
            print("Raw fields response:", raw_fields)
            raw_fields = self.clean_code_response(raw_fields)
            try:
                selected_fields = json.loads(raw_fields)
                print("Parsed selected fields:", selected_fields)
            except json.JSONDecodeError as e:
                print(f"JSON parsing error for fields: {e}")
                selected_fields = ['name']
        except Exception as e:
            print(f"Error generating fields: {e}")
            selected_fields = ['name']

        selected_fields = [f for f in selected_fields if f in available_fields]
        print("Filtered selected fields:", selected_fields)
        if not selected_fields:
            selected_fields = ['name']
            print("No valid fields found after filtering. Defaulting to ['name'].")

        try:
            print("Generating domain filter based on question, model and selected fields...")
            domain_response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an AI assistant specialized in Odoo. "
                            "Based on the user's question, the chosen model, and the selected fields, "
                            "generate an appropriate domain filter in JSON format. "
                            "The domain should be a list of tuples (e.g., [['field', '=', 'value']]). "
                            "If no domain is needed, return an empty list []. Provide only valid JSON."
                        )
                    },
                    {
                        "role": "user",
                        "content": f"Question: '{question}'\nModel: '{valid_model}'\nSelected fields: {selected_fields}"
                    }
                ]
            )
            raw_domain = domain_response.choices[0].message.content.strip()
            print("Raw domain response:", raw_domain)
            raw_domain = self.clean_code_response(raw_domain)
            try:
                domain_filter = json.loads(raw_domain)
                print("Parsed domain filter:", domain_filter)
            except json.JSONDecodeError as e:
                print(f"JSON parsing error for domain: {e}")
                domain_filter = []
        except Exception as e:
            print(f"Error generating domain: {e}")
            domain_filter = []

        try:
            print("Generating SQL query based on model, fields and domain...")
            sql_response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an AI assistant specialized in Odoo. "
                            "Using the given model, selected fields, and domain filter, generate a complete SQL SELECT query "
                            "that can be executed to retrieve the relevant data from the database. "
                            "Ensure the query is syntactically correct and provide only the SQL query without any additional explanation."
                        )
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Question: '{question}'\nModel: '{valid_model}'\n"
                            f"Selected fields: {selected_fields}\nDomain: {domain_filter}"
                        )
                    }
                ]
            )
            raw_sql = sql_response.choices[0].message.content.strip()
            print("Raw SQL response:", raw_sql)
            sql_query = self.clean_code_response(raw_sql)
            print("Final SQL query:", sql_query)
        except Exception as e:
            print(f"Error generating SQL query: {e}")
            sql_query = ""

        print("--- Finished generate_model_fields_and_domain_query ---\n")
        return {
            'model': valid_model,
            'fields': selected_fields,
            'domain': domain_filter,
            'sql_query': sql_query,
        }

    def execute_sql_query(self, sql_query):
        print("Executing SQL query:", sql_query)
        try:
            self.env.cr.execute(sql_query)
            results = self.env.cr.fetchall()
            print("SQL query executed successfully. Results:", results)
            return results
        except Exception as e:
            print(f"Error executing SQL query: {e}")
            return None

    def format_results_for_display(self, results, selected_fields):
        try:
            if results:
                formatted = "تم العثور على النتائج التالية:\n\n"
                for rec in results:
                    for index, field in enumerate(selected_fields):
                        value = rec[index] if index < len(rec) else "غير متوفر"
                        formatted += f"{field.capitalize()}: {value}\n"
                    formatted += "\n"
                formatted += "الرجاء مراجعة النتائج أعلاه لمزيد من التفاصيل."
                return formatted
            else:
                return "لم يتم العثور على سجلات."
        except Exception as e:
            print(f"Error formatting results: {e}")
            return "حدث خطأ أثناء تنسيق النتائج."

    def compute_answer_action(self):
        for record in self:
            if record.question:
                print("\n--- Starting compute_answer_action ---")
                generated = self.generate_model_fields_and_domain_query(record.question)
                if not generated:
                    record.answer = " فشل في توليد أجزاء الاستعلام."
                    print("Failed to generate query parts.")
                    continue

                model = generated.get('model', 'res.partner')
                selected_fields = generated.get('fields', ['name'])
                domain_filter = generated.get('domain', [])
                sql_query = generated.get('sql_query', "")

                record.answer = (
                    f"Model: {model}\n"
                    f"Selected Fields: {selected_fields}\n"
                    f"Domain: {domain_filter}\n"
                    f"SQL Query: {sql_query}"
                )
                print("Generated query details set in answer field.")

                if sql_query:
                    results = self.execute_sql_query(sql_query)
                    if results:
                        record.answer = self.format_results_for_display(results, selected_fields)
                        print("Query executed and results formatted.")
                    else:
                        manual_instructions = self.get_manual_search_instructions(model, record.question)
                        record.answer = (
                            " لم يتم العثور على نتائج.\n\n"
                            "إليك تعليمات البحث اليدوي:\n\n" + manual_instructions
                        )
                        print("No results found; manual instructions provided.")
                else:
                    record.answer = " لم يتم توليد استعلام SQL صالح."
                    print("No valid SQL query was generated.")
                print("--- Finished compute_answer_action ---\n")


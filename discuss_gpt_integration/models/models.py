from odoo import models, api


class ChatGPTDiscussIntegration(models.AbstractModel):
    _inherit = 'mail.thread'

    # لا نحتاج لتعريف _name هنا، لأننا نعمل على نموذج مجرد

    @api.model
    def message_post(self, **kwargs):
        # حفظ محتوى الرسالة المُرسلة
        user_message = kwargs.get('body', '')
        # استدعاء الوظيفة الأصلية لإرسال الرسالة
        result = super(ChatGPTDiscussIntegration, self).message_post(**kwargs)

        # مثال: التحقق من أن الرسالة تبدأ بكلمة مفتاحية مثل "/gpt"
        if user_message.strip().startswith("/gpt"):
            # إزالة البادئة من الرسالة
            clean_message = user_message.strip()[4:].strip()
            if clean_message:
                # إنشاء سجل في chatgpt.module لتنفيذ منطق ChatGPT
                chatgpt_module = self.env['chatgpt.module'].create({
                    'question': clean_message,
                })
                chatgpt_module.compute_answer_action()
                bot_answer = chatgpt_module.answer or "لم يتم توليد إجابة."

                # نشر الرد في نفس chatter باستخدام الدالة الأصلية message_post
                super(ChatGPTDiscussIntegration, self).message_post(
                    body=bot_answer,
                    message_type='comment',
                    subtype_xmlid='mail.mt_comment',
                )

        return result

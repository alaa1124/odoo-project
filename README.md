### Project Task Hierarchy
#### 1. Task and Sub-task Ordering
Create a function to order tasks and sub-tasks, ensuring sub-tasks are always displayed under their parent task.
- Details:
	- Ensure that tasks and sub-tasks maintain a hierarchical order in the tree view, with sub-tasks indented beneath parent tasks.
- Module name: test_project_task_hierarchy
#### 2. Tree View Hierarchy 
Modify the tree view to visually display a task-sub-task hierarchy.
- Details:
	- Dynamically expand/collapse the tree structure to visually represent the task hierarchy.
- Module name: test_project_task_hierarchy
### Sales Requirement
#### 1. Restrict Salesperson Changes
Only managers are allowed to change the salesperson on a sale order.
- Details:
	- Implement a restriction that prevents non-managerial users from modifying the salesperson field in a sale order.
	- This should be enforced in both the form view and backend logic.
- Module name: test_sale_restrict_sales_person
#### 2. Security and Access Control
Implement record-level access control for sale orders, restricting visibility based on the user's assigned sales team.
- Sale Orders:
	- Managers: Can view and edit all sale orders.
	- Salespersons: Can only view and edit sale orders from their own team.
- Details:
	- Implement record rules and user groups to enforce these restrictions.
	- Ensure the restriction applies in both the UI and backend logic to prevent unauthorized access.
- Module name: test_sale_restict_sales_person
### Product/MRP Requirement
#### 1. Product Name Update
Automatically update product names to include the MRP tag if the route is set to Manufacturing.
- Details:
	- Example:
Before: [E-COM11] Cabinet with Doors
After: [E-COM11][MRP] Cabinet with Doors
	- This should apply only to products that have the "Manufacturing" route enabled.
- Module name: test_product_is_mrp
### Website Requirement
#### 1. Partner Highlight Snippet
Create a website snippet that allows the admin to highlight their top partners.
- Details:
	- The snippet should be configurable via the website builder and allow the slection of the partner via Boolean field in the backend.
- Module name: test_highlight_partners
### Automated Email Notifications
#### 1. Email Notification for Invoiced Sale Orders
Create an automated action to send an email to the salesperson when a sale order moves to the "Invoiced" stage.
- Details:
	- The email should include key sale order details like the sale order number, total, and invoice status.
- Module name: test_sale_order_notifications


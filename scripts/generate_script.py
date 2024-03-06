import json

# def generate_ansible_script(json_data):
#     # Ansible playbook template
#     ansible_template = """
# ---
# - name: Process Use Case
#   hosts: localhost
#   gather_facts: false

#   tasks:
#     - name: Extracting information from input
#       set_fact:
#         use_case_id: "{{ input_data.use_case_id }}"
#         status: "{{ input_data.status }}"
#         domain: "{{ input_data.domain }}"
#         db_name: "{{ input_data.updated_form_data.db_name }}"
#         db_engine: "{{ input_data.updated_form_data.db_engine }}"
#         db_user: "{{ input_data.updated_form_data.db_user }}"
#         question_0: "{{ input_data.updated_form_data['question_0_What is the name of the database you want to create?'] }}"
#         question_1: "{{ input_data.updated_form_data['question_1_Which database engine would you like to use?'] }}"
#         question_2: "{{ input_data.updated_form_data['question_2_Provide a username for the database.'] }}"
#         question_3: "{{ input_data.updated_form_data['question_3_Do you want to set a password for the database user?'] }}"
#         category_name: "{{ input_data.category.name }}"

#     - name: Add TODO comments based on values
#       debug:
#         msg: |
#           TODO:
#           - Use Case ID: {{ use_case_id }}
#           - Status: {{ status }}
#           - Domain: {{ domain }}
#           - Database Name: {{ db_name }}
#           - Database Engine: {{ db_engine }}
#           - Database User: {{ db_user }}
#           - Question 0: {{ question_0 }}
#           - Question 1: {{ question_1 }}
#           - Question 2: {{ question_2 }}
#           - Question 3: {{ question_3 }}
#           - Category Name: {{ category_name }}
# """

#     # Replace values in the Ansible script template
#     ansible_script = ansible_template.replace("{{ input_data.use_case_id }}", str(json_data["use_case_id"]))
#     ansible_script = ansible_script.replace("{{ input_data.status }}", json_data["status"])
#     ansible_script = ansible_script.replace("{{ input_data.domain }}", json_data["domain"])
#     ansible_script = ansible_script.replace("{{ input_data.updated_form_data.db_name }}", json_data["updated_form_data"]["db_name"])
#     ansible_script = ansible_script.replace("{{ input_data.updated_form_data.db_engine }}", json_data["updated_form_data"]["db_engine"])
#     ansible_script = ansible_script.replace("{{ input_data.updated_form_data.db_user }}", json_data["updated_form_data"]["db_user"])
#     ansible_script = ansible_script.replace("{{ input_data.updated_form_data['question_0_What is the name of the database you want to create?'] }}", json_data["updated_form_data"]["question_0_What is the name of the database you want to create?"])
#     ansible_script = ansible_script.replace("{{ input_data.updated_form_data['question_1_Which database engine would you like to use?'] }}", json_data["updated_form_data"]["question_1_Which database engine would you like to use?"])
#     ansible_script = ansible_script.replace("{{ input_data.updated_form_data['question_2_Provide a username for the database.'] }}", json_data["updated_form_data"]["question_2_Provide a username for the database."])
#     ansible_script = ansible_script.replace("{{ input_data.updated_form_data['question_3_Do you want to set a password for the database user?'] }}", json_data["updated_form_data"]["question_3_Do you want to set a password for the database user?"])
#     ansible_script = ansible_script.replace("{{ input_data.category.name }}", json_data["category"]["name"])

#     # Save the Ansible script with the filename based on use_case_id
#     filename = f"ansible_script_{json_data['use_case_id']}.yaml"
#     with open(filename, "w") as file:
#         file.write(ansible_script)

#     print(f"Ansible script saved as: {filename}")

def generate_ansible_script(json_data):
    # Ansible playbook template
    ansible_template = """
---
- name: Process Use Case
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Extracting information from input
      set_fact:
{set_fact_content}
    - name: Add TODO comments based on values
      debug:
        msg: |
          TODO:
{debug_content}
"""

    # Generate set_fact and debug sections dynamically based on JSON data
    set_fact_content = ""
    debug_content = ""
    for key, value in json_data.items():
        if isinstance(value, dict):
            for nested_key, nested_value in value.items():
                set_fact_content += f"        {nested_key}: '{nested_value}'\n"
                debug_content += f"          - {nested_key}: {{ {nested_key} }}\n"
        else:
            set_fact_content += f"        {key}: '{value}'\n"
            debug_content += f"          - {key}: {{ {key} }}\n"

    # Replace values in the Ansible script template
    ansible_script = ansible_template.format(set_fact_content=set_fact_content, debug_content=debug_content)

    # Save the Ansible script with the filename based on use_case_id
    filename = f"ansible_script_{json_data.get('use_case_id', 'unknown')}.yaml"
    with open(filename, "w") as file:
        file.write(ansible_script)

    print(f"Ansible script saved as: {filename}")

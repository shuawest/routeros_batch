# Ansible Collection - shuawest.routeros_batch

Modules for MikroTik RouterOS idempotent script generation, script execution, and batch fact retrieval

NOTE: This collection is not supported - use at your own risk

# TODO
 
X Add community.routeros as dependency of shuawest.routeros_batch
- setup mini mtk router to have 192.168.1.11 ip address for testing while traveling
- create class that derives ROS_api_module to add, remove, and execute scripts in a module as they are in milabs-depict-ansible
  - determine if extending or composing api module is appropriate
X test module with integration tests 
- use the routeros mock testing modules to create unit tests
- create batch_facts module that extends ROS_api_info module to reach list of facts and return results in structured format
- determine if there is a way to srape the schema data points from the device

# Research
- Call an ansible module from a module
  https://stackoverflow.com/questions/46893066/calling-an-ansible-module-from-another-ansible-module

- Developing modules
  https://docs.ansible.com/ansible/latest/dev_guide/developing_modules.html#building-testing

- Is it possible to call a module from a module?
  https://groups.google.com/g/ansible-devel/c/-UJW__6CYCo 

- Action plugin - how to write
  https://docs.ansible.com/ansible/latest/dev_guide/developing_plugins.html#action-plugins 
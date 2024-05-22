# Ansible Collection - shuawest.routeros_batch

Modules for MikroTik RouterOS idempotent script generation, script execution, and batch fact retrieval

NOTE: This collection is not supported - use at your own risk

# TODO
 
- fix catching of exceptions - when failed flag is true, the module should report a failure and error
- add document generation and document to galaxy levels
- consider a reconcile module that uses commands to generate and execute a script, then compare the batch fetch of the paths
to validate settings. 
- add removal of field values (! & null) in the commands
- determine if it's possible to capture console output of a ros script
- determine if it's possible to have scripts output logs 
- build unit testing with mocks for action modules 
- determine if there is a way to srape the schema data points from the device


X Add community.routeros as dependency of shuawest.routeros_batch
X create class that derives ROS_api_module to add, remove, and execute scripts in a module as they are in milabs-depict-ansible
  X determine if extending or composing api module is appropriate
X test module with integration tests 
X create batch_facts module that extends ROS_api_info module to reach list of facts and return results in structured format
- setup mini mtk router to have 192.168.1.11 ip address for testing while traveling

# Research
- Call an ansible module from a module
  https://stackoverflow.com/questions/46893066/calling-an-ansible-module-from-another-ansible-module

- Developing modules
  https://docs.ansible.com/ansible/latest/dev_guide/developing_modules.html#building-testing

- Is it possible to call a module from a module?
  https://groups.google.com/g/ansible-devel/c/-UJW__6CYCo 

- Action plugin - how to write
  https://docs.ansible.com/ansible/latest/dev_guide/developing_plugins.html#action-plugins 
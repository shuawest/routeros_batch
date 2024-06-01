# Ansible Collection - shuawest.routeros_batch

Modules for MikroTik RouterOS idempotent script generation, script execution, and batch fact retrieval

NOTE: This collection is not supported - use at your own risk

# TODO
 
- add batch fasts integration tests
- add removal of field values (! & null) in the commands
- execution validation:
  - consider a reconcile module that uses commands to generate and execute a script, then compare the batch fetch of the paths
  to validate settings. 
  - determine if it's possible to capture console output of a ros script 
  - determine if it's possible to have scripts output logs
  - determine if there is a way to scrape the schema data points from the device
  - explore using ssh to submit commands (facts module limits objects that can be queried)
- build unit testing with mocks for action modules 


x add document generation and document to galaxy levels
x setup mini mtk router for testing while traveling
X increase minor version of module and release
X separate integration tests into task files
X fix catching of exceptions - when failed flag is true, the module should report a failure and error
X Add community.routeros as dependency of shuawest.routeros_batch
X create class that derives ROS_api_module to add, remove, and execute scripts in a module as they are in milabs-depict-ansible
  X determine if extending or composing api module is appropriate
X test module with integration tests 
X create batch_facts module that extends ROS_api_info module to reach list of facts and return results in structured format

# Research
- Call an ansible module from a module
  https://stackoverflow.com/questions/46893066/calling-an-ansible-module-from-another-ansible-module

- Developing modules
  https://docs.ansible.com/ansible/latest/dev_guide/developing_modules.html#building-testing

- Is it possible to call a module from a module?
  https://groups.google.com/g/ansible-devel/c/-UJW__6CYCo 

- Action plugin - how to write
  https://docs.ansible.com/ansible/latest/dev_guide/developing_plugins.html#action-plugins 

# Removed from docs

script state options
- `present` - add or update the script on the default, but not execute it
- `absent` - remove the script from the device
- `executed` - execute script already on the device
- `executed_once` - add or update the script, execute it
- `executed_clean` - add or update the script, execute it, then remove it from the device

script sample
    sample:
- "; ### present: Put VPN bridge 'bridge' ### ;\n\n:if ([:len [/interface bridge find name=\\\"bridge\\\" ]] > 0) do={\n\t/interface bridge set [ find name=\\\"bridge\\\" ] name=\\\"bridge\\\" fast-forward=no \n} else={\n\t/interface bridge add name=\\\"bridge\\\" fast-forward=no \n}\n\n\n; ### absent: Remove VPN user 'guest' ### ;\n\n:if ([:len [/ppp secret find name=\\\"guest\\\" ]] > 0) do={\n\t/ppp secret remove [ find name=\\\"guest\\\" ]\n}\n\n\n",

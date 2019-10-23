# private key
key_path="~/.ssh/key1"
key_name="key1"

# openstack
username="admin"
auth_url="http://x.x.x.x/identity"
user_domain_name="default"

# working-example 1
project_name1="working1"
project_id1="xxx"

we-create:
	test -f ~/we-inputs.yaml || echo "private_key_path: $(key_path)\nprivate_key_name: $(key_name)\nopenstack_config: {}" > ~/we-inputs.yaml
	aria service-templates store working-example1/we.yaml we
	aria services create -t we we_service -i ~/we-inputs.yaml -vvv

we-install:
	grep \"$(project_name1)\" ~/openstack_config.json || (read -p "$(username)@($auth_url) password: " pass && echo "{\n\"username\": \"$(username)\",\n\"password\": \"$$pass\",\n\"project_name\": \"$(project_name1)\",\n\"project_id\": \"$(project_id1)\",\n\"auth_url\": \"$(auth_url)\",\n\"user_domain_name\": \"$(user_domain_name)\"\n}" > ~/openstack_config.json)
	aria executions start install -s we_service -vv

we-uninstall:
	aria executions start uninstall -s we_service -vvv

we-delete:
	@echo -n "Are you sure? [y/N] " && read ans && [ $${ans:-N} = y ]
	aria services delete we_service -f
	aria service-templates delete we

we-validate:
	aria execution start validate -s we_service -vvv

we-test:
	aria execution start test -s we_service -vvv

we-graph:
	aria executions start creategraph -s we_service -vv

we-replace: we-delete we-create

# working-example 2
project_name2="working2"
project_id2="xxx"

we2-create:
	test -f ~/we-inputs.yaml || echo "private_key_path: $(key_path)\nprivate_key_name: $(key_name)\nopenstack_config: {}" > ~/we-inputs.yaml
	aria service-templates store working-example2/we2.yaml we2
	aria services create -t we2 we2_service -i ~/we-inputs.yaml -vvv


we2-install:
	grep \"$(project_name2)\" ~/openstack_config.json || (read -p "$(username)@$(auth_url) password: " pass && echo "{\n\"username\": \"$(username)\",\n\"password\": \"$$pass\",\n\"project_name\": \"$(project_name2)\",\n\"project_id\": \"$(project_id2)\",\n\"auth_url\": \"$(auth_url)\",\n\"user_domain_name\": \"$(user_domain_name)\"\n}" > ~/openstack_config.json)
	aria executions start install -s we2_service -vv

we2-delete:
	@echo -n "Are you sure? [y/N] " && read ans && [ $${ans:-N} = y ]
	aria services delete we2_service -f
	aria service-templates delete we2

we2-validate:
	aria execution start validate -s we2_service -vvv

we2-test:
	aria execution start test -s we2_service -vvv

we2-graph:
	aria executions start creategraph -s we2_service -vv

we2-replace: we2-delete we2-create

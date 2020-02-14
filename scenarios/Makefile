# private key
key_path="~/.ssh/ex1-sdl"
key_name="ex1"

# openstack
username="admin"
auth_url="http://10.186.37.4/identity"
user_domain_name="default"

# Scenario 1 (working-example 1)
project_name1="working1"
project_id1="4ddc6334192a437d835149fb5da7b094"

we1-create:
	test -f ~/we-inputs.yaml || echo "private_key_path: $(key_path)\nprivate_key_name: $(key_name)\nopenstack_config: {}" > ~/we-inputs.yaml
	aria service-templates store scenario1/scenario.yaml we
	aria services create -t we we_service -i ~/we-inputs.yaml -vvv

we1-install:
	grep \"$(project_name1)\" ~/openstack_config.json || (read -p "$(username)@($auth_url) password: " pass && echo "{\n\"username\": \"$(username)\",\n\"password\": \"$$pass\",\n\"project_name\": \"$(project_name1)\",\n\"project_id\": \"$(project_id1)\",\n\"auth_url\": \"$(auth_url)\",\n\"user_domain_name\": \"$(user_domain_name)\"\n}" > ~/openstack_config.json)
	aria executions start install -s we_service -vv

we1-uninstall:
	aria executions start uninstall -s we_service -vvv

we1-delete:
	@echo -n "Are you sure? [y/N] " && read ans && [ $${ans:-N} = y ]
	aria services delete we_service -f
	aria service-templates delete we

we1-verify:
	date
	date +%s%3N
	aria execution start verify -s we_service -vvv
	date
	date +%s%3N

we1-test:
	date
	date +%s%3N
	aria execution start test -s we_service -vvv
	date
	date +%s%3N

we1-graph:
	aria executions start creategraph -s we_service -vv

we1-replace: we1-delete we1-create

# Scenario 2 (working-example 2)
project_name2="working2"
project_id2="a860dfcfbcf342ea92e75edcd20f0aa9"

we2-create:
	test -f ~/we-inputs.yaml || echo "private_key_path: $(key_path)\nprivate_key_name: $(key_name)\nopenstack_config: {}" > ~/we-inputs.yaml
	aria service-templates store scenario2/scenario.yaml we2
	aria services create -t we2 we2_service -i ~/we-inputs.yaml -vvv


we2-install:
	grep \"$(project_name2)\" ~/openstack_config.json || (read -p "$(username)@$(auth_url) password: " pass && echo "{\n\"username\": \"$(username)\",\n\"password\": \"$$pass\",\n\"project_name\": \"$(project_name2)\",\n\"project_id\": \"$(project_id2)\",\n\"auth_url\": \"$(auth_url)\",\n\"user_domain_name\": \"$(user_domain_name)\"\n}" > ~/openstack_config.json)
	aria executions start install -s we2_service -vv

we2-delete:
	@echo -n "Are you sure? [y/N] " && read ans && [ $${ans:-N} = y ]
	aria services delete we2_service -f
	aria service-templates delete we2

we2-verify:
	date
	date +%s%3N
	aria execution start verify -s we2_service -vvv
	date
	date +%s%3N

we2-test:
	date
	date +%s%3N
	aria execution start test -s we2_service -vvv
	date
	date +%s%3N

we2-graph:
	aria executions start creategraph -s we2_service -vv

we2-replace: we2-delete we2-create

# Scenario 3 (working-example 3)
project_name3="working3"
project_id3="af0c6a40f4854a8787d3436d1719ddc9"

we3-create:
	test -f ~/we-inputs.yaml || echo "private_key_path: $(key_path)\nprivate_key_name: $(key_name)\nopenstack_config: {}" > ~/we-inputs.yaml
	aria service-templates store scenario3/scenario.yaml we3
	aria services create -t we3 we3_service -i ~/we-inputs.yaml -vvv

we3-install:
	grep \"$(project_name3)\" ~/openstack_config.json || (read -p "$(username)@$(auth_url) password: " pass && echo "{\n\"username\": \"$(username)\",\n\"password\": \"$$pass\",\n\"project_name\": \"$(project_name3)\",\n\"project_id\": \"$(project_id3)\",\n\"auth_url\": \"$(auth_url)\",\n\"user_domain_name\": \"$(user_domain_name)\"\n}" > ~/openstack_config.json)
	aria executions start install -s we3_service -vv

we3-delete:
	@echo -n "Are you sure? [y/N] " && read ans && [ $${ans:-N} = y ]
	aria services delete we3_service -f
	aria service-templates delete we3

we3-verify:
	date
	date +%s%3N
	aria execution start verify -s we3_service -vvv
	date
	date +%s%3N

we3-test:
	date
	date +%s%3N
	aria execution start test -s we3_service -vvv
	date
	date +%s%3N

we3-graph:
	aria executions start creategraph -s we3_service -vv

we3-replace: we3-delete we3-create

# Scenario 4 (working-example 4)
project_name4="working4"
project_id4="5b8fe4e9d68e41949eda1a81e8062292"

we4-create:
	test -f ~/we-inputs.yaml || echo "private_key_path: $(key_path)\nprivate_key_name: $(key_name)\nopenstack_config: {}" > ~/we-inputs.yaml
	aria service-templates store scenario4/scenario.yaml we4
	aria services create -t we4 we4_service -i ~/we-inputs.yaml -vvv

we4-install:
	grep \"$(project_name4)\" ~/openstack_config.json || (read -p "$(username)@$(auth_url) password: " pass && echo "{\n\"username\": \"$(username)\",\n\"password\": \"$$pass\",\n\"project_name\": \"$(project_name4)\",\n\"project_id\": \"$(project_id4)\",\n\"auth_url\": \"$(auth_url)\",\n\"user_domain_name\": \"$(user_domain_name)\"\n}" > ~/openstack_config.json)
	aria executions start install -s we4_service -vv

we4-delete:
	@echo -n "Are you sure? [y/N] " && read ans && [ $${ans:-N} = y ]
	aria services delete we4_service -f
	aria service-templates delete we4

we4-verify:
	date
	date +%s%3N
	aria execution start verify -s we4_service -vvv
	date
	date +%s%3N

we4-test:
	date
	date +%s%3N
	aria execution start test -s we4_service -vvv
	date
	date +%s%3N

we4-graph:
	aria executions start creategraph -s we4_service -vv

we4-replace: we4-delete we4-create

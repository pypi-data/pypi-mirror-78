HOW to deploy
-------------

To deploy |project| in a cluster:

1. Prepare config files ``lagent.conf`` and ``lmaster.conf``
2. Prepare a host file for Ansible
3. Install Python. If using a Redhat-like system, it can be done with:

   .. code-block:: console

      $ ansible-playbook -e restricted_hosts=only-two provisioning-on-nodes.yml
   
4. Deploy |project|:

   .. code-block:: console

      $ ansible-playbook install.yml
      
5. Start ``lmaster``:

   .. code-block:: console
		   
      $ ansible-plabook start-lmaster.yml

6. Start ``lagent``:

   .. code-block:: console

      $ ansible-plabook start-lagent.yml


from tenable.io import TenableIO
tio = TenableIO('', '')

tio.tags.create('Operating System', 'Windows',
     filters=[('operating_system', 'match', ['Windows'])])
tio.tags.create('Operating System', 'Windows XP',
     filters=[('operating_system', 'match', ['Windows XP'])])
tio.tags.create('Operating System', 'Windows Vista',
     filters=[('operating_system', 'match', ['Windows Vista'])])
tio.tags.create('Operating System', 'Windows 7',
     filters=[('operating_system', 'match', ['Windows 7'])])
tio.tags.create('Operating System', 'Windows 8',
     filters=[('operating_system', 'match', ['Windows 8'])])
tio.tags.create('Operating System', 'Windows 10',
     filters=[('operating_system', 'match', ['Windows 10'])])
tio.tags.create('Operating System', 'Windows 11',
     filters=[('operating_system', 'match', ['Windows 11'])])
tio.tags.create('Operating System', 'Windows Server',
     filters=[('operating_system', 'match', ['Windows Server'])])
tio.tags.create('Operating System', 'Windows Server 2003',
     filters=[('operating_system', 'match', ['Windows Server 2003'])])
tio.tags.create('Operating System', 'Windows Server 2008',
     filters=[('operating_system', 'match', ['Windows Server 2008'])])
tio.tags.create('Operating System', 'Windows Server 2012',
     filters=[('operating_system', 'match', ['Windows Server 2012'])])
tio.tags.create('Operating System', 'Windows Server 2016',
     filters=[('operating_system', 'match', ['Windows Server 2016'])])
tio.tags.create('Operating System', 'Windows Server 2019',
     filters=[('operating_system', 'match', ['Windows Server 2019'])])
tio.tags.create('Operating System', 'Windows Server 2022',
     filters=[('operating_system', 'match', ['Windows Server 2022'])])
tio.tags.create('Operating System', 'Linux',
     filters=[('operating_system', 'match', ['Linux'])])
tio.tags.create('Operating System', 'Linux - CentOS',
     filters=[('operating_system', 'match', ['CentOS'])])
tio.tags.create('Operating System', 'Linux - Debian',
     filters=[('operating_system', 'match', ['Debian'])])
tio.tags.create('Operating System', 'Linux - Red Hat',
     filters=[('operating_system', 'match', ['Red Hat'])])
tio.tags.create('Operating System', 'Linux - Ubuntu',
     filters=[('operating_system', 'match', ['Ubuntu'])])
tio.tags.create('Operating System', 'Linux - UNIX',
     filters=[('operating_system', 'match', ['UNIX'])])
tio.tags.create('Operating System', 'VMware',
     filters=[('operating_system', 'match', ['VMware'])])
tio.tags.create('Operating System', 'VMware vCenter',
     filters=[('operating_system', 'match', ['VMware vCenter'])])
tio.tags.create('Operating System', 'VMware ESXi',
     filters=[('operating_system', 'match', ['VMware ESXi'])])
tio.tags.create('Operating System', 'Nutanix',
     filters=[('operating_system', 'match', ['Nutanix'])])
tio.tags.create('Operating System', 'ExtremeXOS',
     filters=[('operating_system', 'match', ['ExtremeXOS'])])
tio.tags.create('Operating System', 'Fortigate',
     filters=[('operating_system', 'match', ['Fortigate'])])
tio.tags.create('Operating System', 'Fortinet',
     filters=[('operating_system', 'match', ['Fortinet'])])
tio.tags.create('Operating System', 'Cisco',
     filters=[('operating_system', 'match', ['Cisco'])])
tio.tags.create('Operating System', 'Linksys',
     filters=[('operating_system', 'match', ['Linksys'])])
tio.tags.create('Operating System', '3Com',
     filters=[('operating_system', 'match', ['3Com'])])
tio.tags.create('Operating System', 'Android',
     filters=[('operating_system', 'match', ['Android'])])
tio.tags.create('Operating System', 'Check Point',
     filters=[('operating_system', 'match', ['Check Point'])])
tio.tags.create('Operating System', 'Palo Alto',
     filters=[('operating_system', 'match', ['Palo Alto'])])
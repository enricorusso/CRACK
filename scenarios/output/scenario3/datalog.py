
import logging
from pyDatalog import pyDatalog
from pyDatalog import pyEngine
pyEngine.Logging = True
logging.basicConfig(level=logging.INFO)
    
    
pyDatalog.create_terms('isConnected,hostACL,A,existsRoute,knows,hasAccount,H,K,M,hasUser,N,Q,P,S,listeningOn,U,T,V,X,isRouter,ID6,ID4,ID5,ID2,ID3,ID1,R')

## videoserver_1 ##
#  videoserver_system_1 (sdl.nodes.System.Linux),isConnected
+ isConnected(1,'videoserver_1', 'Server_subnet_1')


## Firewall_1 ##
#  Firewall_UFW_1 (sdl.nodes.Firewall.UFW),existsRoute
+ existsRoute(2,'Server_subnet_1','Server_subnet_1','Firewall_1')
#  Firewall_UFW_1 (sdl.nodes.Firewall.UFW),existsRoute
+ existsRoute(2,'Server_subnet_1','Outside_subnet_1','Firewall_1')
#  Firewall_UFW_1 (sdl.nodes.Firewall.UFW),existsRoute
+ existsRoute(2,'Server_subnet_1','DMZ_subnet_1','Firewall_1')
#  Firewall_UFW_1 (sdl.nodes.Firewall.UFW),existsRoute
+ existsRoute(2,'Server_subnet_1','IoT_subnet_1','Firewall_1')
#  Firewall_UFW_1 (sdl.nodes.Firewall.UFW),existsRoute
+ existsRoute(2,'Outside_subnet_1','Server_subnet_1','Firewall_1')
#  Firewall_UFW_1 (sdl.nodes.Firewall.UFW),existsRoute
+ existsRoute(2,'Outside_subnet_1','Outside_subnet_1','Firewall_1')
#  Firewall_UFW_1 (sdl.nodes.Firewall.UFW),existsRoute
+ existsRoute(2,'Outside_subnet_1','DMZ_subnet_1','Firewall_1')
#  Firewall_UFW_1 (sdl.nodes.Firewall.UFW),existsRoute
+ existsRoute(2,'Outside_subnet_1','IoT_subnet_1','Firewall_1')
#  Firewall_UFW_1 (sdl.nodes.Firewall.UFW),existsRoute
+ existsRoute(2,'DMZ_subnet_1','Server_subnet_1','Firewall_1')
#  Firewall_UFW_1 (sdl.nodes.Firewall.UFW),existsRoute
+ existsRoute(2,'DMZ_subnet_1','Outside_subnet_1','Firewall_1')
#  Firewall_UFW_1 (sdl.nodes.Firewall.UFW),existsRoute
+ existsRoute(2,'DMZ_subnet_1','DMZ_subnet_1','Firewall_1')
#  Firewall_UFW_1 (sdl.nodes.Firewall.UFW),existsRoute
+ existsRoute(2,'DMZ_subnet_1','IoT_subnet_1','Firewall_1')
#  Firewall_UFW_1 (sdl.nodes.Firewall.UFW),existsRoute
+ existsRoute(2,'IoT_subnet_1','Server_subnet_1','Firewall_1')
#  Firewall_UFW_1 (sdl.nodes.Firewall.UFW),existsRoute
+ existsRoute(2,'IoT_subnet_1','Outside_subnet_1','Firewall_1')
#  Firewall_UFW_1 (sdl.nodes.Firewall.UFW),existsRoute
+ existsRoute(2,'IoT_subnet_1','DMZ_subnet_1','Firewall_1')
#  Firewall_UFW_1 (sdl.nodes.Firewall.UFW),existsRoute
+ existsRoute(2,'IoT_subnet_1','IoT_subnet_1','Firewall_1')
#  Firewall_UFW_1 (sdl.nodes.Firewall.UFW),isConnected
+ isConnected(3,'Firewall_1', 'Server_subnet_1')
#  Firewall_UFW_1 (sdl.nodes.Firewall.UFW),isConnected
+ isConnected(3,'Firewall_1', 'Outside_subnet_1')
#  Firewall_UFW_1 (sdl.nodes.Firewall.UFW),isConnected
+ isConnected(3,'Firewall_1', 'DMZ_subnet_1')
#  Firewall_UFW_1 (sdl.nodes.Firewall.UFW),isConnected
+ isConnected(3,'Firewall_1', 'IoT_subnet_1')
#  Firewall_UFW_1 (sdl.nodes.Firewall.UFW),isRouter
+ isRouter(4,'Firewall_1')
#  Firewall_DefaultRoute1_1 (sdl.nodes.Configuration.DefaultRoute.Firewall.UFW),existsRoute
existsRoute(5,'Outside_subnet_1', N, 'Firewall_1') <= isConnected(ID1,X, 'Outside_subnet_1') & isRouter(ID2,X) & existsRoute(ID3,'Outside_subnet_1', N, X)


## cam1_1 ##
#  cam1_system_1 (sdl.nodes.System.Linux),isConnected
+ isConnected(6,'cam1_1', 'Server_subnet_1')


## invariant_1 ##
#  invariant_1 (sdl.nodes.Invariant),existsRoute
existsRoute(7,N,M,X) <= isConnected(ID1,X,N) & isConnected(ID2,X,M) & isRouter(ID3,X)
#  invariant_1 (sdl.nodes.Invariant),hostACL1
hostACL(8,H,K,P,Q) <= listeningOn(ID1,K,P,Q) & isConnected(ID2,K,N) & isConnected(ID3,H,M) & isConnected(ID4,S,M) & isRouter(ID5,S) & existsRoute(ID6,T,N,S)
#  invariant_1 (sdl.nodes.Invariant),hostACL2
hostACL(9,H,K,P,Q) <= listeningOn(ID1,K,P,Q) & isConnected(ID2,H,N) & isConnected(ID3,K,N)
#  invariant_1 (sdl.nodes.Invariant),hasAccount
hasAccount(10,A,H,U) <= hasUser(ID1,U,H,P,R) & knows(ID2,A,U) & knows(ID3,A,P)


## cam5_1 ##
#  cam5_system_1 (sdl.nodes.System.Linux),isConnected
+ isConnected(11,'cam5_1', 'Server_subnet_1')


## waf_1 ##
#  waf_root_1 (sdl.nodes.User.Linux),hasUser
+ hasUser(12,'waf_root_1', 'waf_1', 'None', 'admin')
#  waf_http_1 (sdl.nodes.Software.Server.HTTP.Linux.Apache),listeningOn
+ listeningOn(13,'waf_1', 'tcp', '80')
#  waf_sysuser1_1 (sdl.nodes.User.Linux),hasUser
+ hasUser(14,'waf_sysuser1_1', 'waf_1', 'None', 'user')
#  waf_system_1 (sdl.nodes.System.Linux),isConnected
+ isConnected(15,'waf_1', 'DMZ_subnet_1')


## cam6_1 ##
#  cam6_system_1 (sdl.nodes.System.Linux),isConnected
+ isConnected(16,'cam6_1', 'IoT_subnet_1')


## climate_1 ##
#  climate_system_1 (sdl.nodes.System.Linux),isConnected
+ isConnected(17,'climate_1', 'IoT_subnet_1')


## ns_1 ##
#  dns_system_1 (sdl.nodes.System.Linux),isConnected
+ isConnected(18,'ns_1', 'DMZ_subnet_1')
#  dns_bind_1 (sdl.nodes.Software.Server.DNS.Linux.Bind),listeningOn
+ listeningOn(19,'ns_1', 'udp', '53')


## siem_1 ##
#  siem_system_1 (sdl.nodes.System.Linux),isConnected
+ isConnected(20,'siem_1', 'Server_subnet_1')


## nas_1 ##
#  nas_system_1 (sdl.nodes.System.Linux),isConnected
+ isConnected(21,'nas_1', 'Server_subnet_1')


## root-ns_1 ##
#  root-ns_bind_1 (sdl.nodes.Software.Server.DNS.Linux.Bind),listeningOn
+ listeningOn(22,'root-ns_1', 'udp', '53')
#  root-ns_system_1 (sdl.nodes.System.Linux),isConnected
+ isConnected(23,'root-ns_1', 'Simint1_subnet_1')


## intranet_1 ##
#  intranet_system_1 (sdl.nodes.System.Linux),isConnected
+ isConnected(24,'intranet_1', 'Server_subnet_1')


## alarm_1 ##
#  alarm_system_1 (sdl.nodes.System.Linux),isConnected
+ isConnected(25,'alarm_1', 'IoT_subnet_1')


## collab_1 ##
#  collab_sysuser1_1 (sdl.nodes.User.Linux),hasUser
+ hasUser(26,'collab_sysuser1_1', 'collab_1', 'None', 'user')
#  collab_http_1 (sdl.nodes.Software.Server.HTTP.Linux.Nginx),listeningOn
+ listeningOn(27,'collab_1', 'tcp', '80')
#  collab_system_1 (sdl.nodes.System.Linux),isConnected
+ isConnected(28,'collab_1', 'DMZ_subnet_1')
#  collab_root_1 (sdl.nodes.User.Linux),hasUser
+ hasUser(29,'collab_root_1', 'collab_1', 'None', 'admin')


## ids_1 ##
#  ids_system_1 (sdl.nodes.System.Linux),isConnected
+ isConnected(30,'ids_1', 'Server_subnet_1')


## dc_1 ##
#  dc_system_1 (sdl.nodes.System.Linux),isConnected
+ isConnected(31,'dc_1', 'Server_subnet_1')


## ftp_1 ##
#  ftp_system_1 (sdl.nodes.System.Linux),isConnected
+ isConnected(32,'ftp_1', 'DMZ_subnet_1')


## www_1 ##
#  www_system_1 (sdl.nodes.System.Linux),isConnected
+ isConnected(33,'www_1', 'DMZ_subnet_1')
#  www_vuln1_1 (sdl.nodes.Vulnerability.Linux.CVE_2019_11043),hasAccount
hasAccount(34,A, 'www_1', 'www_sysuser1_1') <= hasUser(ID1,'www_sysuser1_1', 'www_1', P, R) & listeningOn(ID2,'www_1', 'tcp', '80') & hostACL(ID3,K, 'www_1', 'tcp', '80') & hasAccount(ID4,A, K, V)
#  www_http_1 (sdl.nodes.Software.Server.HTTP.Linux.Nginx),listeningOn
+ listeningOn(35,'www_1', 'tcp', '80')
#  www_sysuser1_1 (sdl.nodes.User.Linux),hasUser
+ hasUser(36,'www_sysuser1_1', 'www_1', 'None', 'user')
#  www_root_1 (sdl.nodes.User.Linux),hasUser
+ hasUser(37,'www_root_1', 'www_1', 'None', 'admin')
#  www_ssh_1 (sdl.nodes.Software.Server.SSH.Linux.OpenSSH),listeningOn
+ listeningOn(38,'www_1', 'tcp', '22')
#  www_user1_1 (sdl.nodes.User.Linux),hasUser
+ hasUser(39,'www_user1_1', 'www_1', '9JmDGEr4', 'user')
#  www_cms_1 (sdl.nodes.Software.Server.CMS.Linux.Wordpress),knows2
knows(40,A, 'venerus') <= hasUser(ID1,'www_sysuser1_1','www_1',P, R) & hasAccount(ID2,A,'www_1', 'www_sysuser1_1')
#  www_cms_1 (sdl.nodes.Software.Server.CMS.Linux.Wordpress),knows1
knows(41,A, 'venerus') <= hasUser(ID1,U,'www_1',P,'admin') & hasAccount(ID2,A,'www_1',U)


## hmi_1 ##
#  hmi_system_1 (sdl.nodes.System.Linux),isConnected
+ isConnected(42,'hmi_1', 'IoT_subnet_1')


## cam3_1 ##
#  cam3_system_1 (sdl.nodes.System.Linux),isConnected
+ isConnected(43,'cam3_1', 'Server_subnet_1')


## db_1 ##
#  db_cmsdb_1 (sdl.nodes.Configuration.DB.Linux.MySQL),knows2
knows(44,A, 'CMS') <= hasUser(ID1,U,'db_1',P,'admin') & hasAccount(ID2,A,'db_1',U)
#  db_cmsdb_1 (sdl.nodes.Configuration.DB.Linux.MySQL),knows1
knows(45,A, 'CMS') <= knows(ID1,A, 'venerus') & hasAccount(ID2,A,H,U) & hostACL(ID3,H, 'db_1', 'tcp', '3306')
#  db_confidentialdb_1 (sdl.nodes.Configuration.DB.Linux.MySQL),knows2
knows(46,A, 'DB_confidential') <= hasUser(ID1,U,'db_1',P,'admin') & hasAccount(ID2,A,'db_1',U)
#  db_confidentialdb_1 (sdl.nodes.Configuration.DB.Linux.MySQL),knows1
knows(47,A, 'DB_confidential') <= knows(ID1,A, 'venerus') & hasAccount(ID2,A,H,U) & hostACL(ID3,H, 'db_1', 'tcp', '3306')
#  db_config_1 (sdl.nodes.Configuration.DBMS.Linux.MySQL.RootAllHosts),listeningOn
+ listeningOn(48,'db_1', 'tcp', '3306')
#  db_system_1 (sdl.nodes.System.Linux),isConnected
+ isConnected(49,'db_1', 'Server_subnet_1')
#  db_collabdb_1 (sdl.nodes.Configuration.DB.Linux.MySQL),knows2
knows(50,A, 'nextcloud') <= hasUser(ID1,U,'db_1',P,'admin') & hasAccount(ID2,A,'db_1',U)
#  db_collabdb_1 (sdl.nodes.Configuration.DB.Linux.MySQL),knows1
knows(51,A, 'nextcloud') <= knows(ID1,A, 'venerus') & hasAccount(ID2,A,H,U) & hostACL(ID3,H, 'db_1', 'tcp', '3306')
#  db_root_1 (sdl.nodes.User.Linux),hasUser
+ hasUser(52,'db_root_1', 'db_1', 'None', 'admin')


## elev_1 ##
#  elev_system_1 (sdl.nodes.System.Linux),isConnected
+ isConnected(53,'elev_1', 'IoT_subnet_1')


## cam4_1 ##
#  cam4_system_1 (sdl.nodes.System.Linux),isConnected
+ isConnected(54,'cam4_1', 'Server_subnet_1')


## client_1 ##
#  eve_1 (sdl.nodes.Principal),hasAccount
+ hasAccount(55,'eve_1', 'client_1','client_user1_1')
#  client_user1_1 (sdl.nodes.User.Linux),hasUser
+ hasUser(56,'client_user1_1', 'client_1', 'supersecret', 'admin')
#  client_system_1 (sdl.nodes.System.Linux),isConnected
+ isConnected(57,'client_1', 'Simint1_subnet_1')


## Provider_1 ##
#  Provider_Route1_1 (sdl.nodes.Configuration.Route.Firewall.VyOS),existsRoute
+ existsRoute(58,'Outside_subnet_1', 'DMZ_subnet_1','Provider_1')
#  Provider_Firewall_1 (sdl.nodes.Firewall.VyOS),existsRoute
+ existsRoute(59,'Extnet_subnet_1','Extnet_subnet_1','Provider_1')
#  Provider_Firewall_1 (sdl.nodes.Firewall.VyOS),existsRoute
+ existsRoute(59,'Extnet_subnet_1','Outside_subnet_1','Provider_1')
#  Provider_Firewall_1 (sdl.nodes.Firewall.VyOS),existsRoute
+ existsRoute(59,'Extnet_subnet_1','Simint1_subnet_1','Provider_1')
#  Provider_Firewall_1 (sdl.nodes.Firewall.VyOS),existsRoute
+ existsRoute(59,'Outside_subnet_1','Extnet_subnet_1','Provider_1')
#  Provider_Firewall_1 (sdl.nodes.Firewall.VyOS),existsRoute
+ existsRoute(59,'Outside_subnet_1','Outside_subnet_1','Provider_1')
#  Provider_Firewall_1 (sdl.nodes.Firewall.VyOS),existsRoute
+ existsRoute(59,'Outside_subnet_1','Simint1_subnet_1','Provider_1')
#  Provider_Firewall_1 (sdl.nodes.Firewall.VyOS),existsRoute
+ existsRoute(59,'Simint1_subnet_1','Extnet_subnet_1','Provider_1')
#  Provider_Firewall_1 (sdl.nodes.Firewall.VyOS),existsRoute
+ existsRoute(59,'Simint1_subnet_1','Outside_subnet_1','Provider_1')
#  Provider_Firewall_1 (sdl.nodes.Firewall.VyOS),existsRoute
+ existsRoute(59,'Simint1_subnet_1','Simint1_subnet_1','Provider_1')
#  Provider_Firewall_1 (sdl.nodes.Firewall.VyOS),isConnected
+ isConnected(60,'Provider_1', 'Extnet_subnet_1')
#  Provider_Firewall_1 (sdl.nodes.Firewall.VyOS),isConnected
+ isConnected(60,'Provider_1', 'Outside_subnet_1')
#  Provider_Firewall_1 (sdl.nodes.Firewall.VyOS),isConnected
+ isConnected(60,'Provider_1', 'Simint1_subnet_1')
#  Provider_Firewall_1 (sdl.nodes.Firewall.VyOS),isRouter
+ isRouter(61,'Provider_1')


## cam2_1 ##
#  cam2_system_1 (sdl.nodes.System.Linux),isConnected
+ isConnected(62,'cam2_1', 'Server_subnet_1')



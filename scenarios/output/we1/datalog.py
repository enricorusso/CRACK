
import logging
from pyDatalog import pyDatalog
from pyDatalog import pyEngine
pyEngine.Logging = True
logging.basicConfig(level=logging.INFO)
    
    
pyDatalog.create_terms('isConnected,hostACL,A,existsRoute,knows,hasAccount,H,K,M,hasUser,N,Q,P,S,listeningOn,U,T,V,X,isRouter,ID6,ID4,ID5,ID2,ID3,ID1,R')

## www_1 ##
#  www_system_1 (sdl.nodes.System.Linux),isConnected
+ isConnected(1,'www_1', 'DMZ_subnet_1')
#  www_root_1 (sdl.nodes.User.Linux),hasUser
+ hasUser(2,'www_root_1', 'www_1', 'None', 'admin')
#  www_ssh_1 (sdl.nodes.Software.Server.SSH.Linux.OpenSSH),listeningOn
+ listeningOn(3,'www_1', 'tcp', '22')
#  www_vuln2_1 (sdl.nodes.Vulnerability.Linux.User.RemoteWeakPassword),hasAccount
hasAccount(4,A, 'www_1', 'www_user1_1') <= knows(ID1,A, 'alice') & hasUser(ID2,'www_user1_1', 'www_1', P, R) & listeningOn(ID3,'www_1', 'tcp', '22') & hostACL(ID4,K, 'www_1', 'tcp', '22') & hasAccount(ID5,A, K, V)
#  www_vuln1_1 (sdl.nodes.Vulnerability.Linux.EOP.APT),hasAccount
hasAccount(5,A, 'www_1', 'www_root_1') <= hasUser(ID1,'www_root_1', 'www_1', P, R) & hasAccount(ID2,A, 'www_1', 'www_user1_1')
#  www_weak1_1 (sdl.nodes.Vulnerability.Linux.User.RemoteEnumerable),knows
knows(6,A, 'alice') <= listeningOn(ID1,'www_1', 'tcp', '80') & hostACL(ID2,K, 'www_1', 'tcp', '80') & hasAccount(ID3,A, K, V)
#  www_user1_1 (sdl.nodes.User.Linux),hasUser
+ hasUser(7,'www_user1_1', 'www_1', 'xexexexe', 'user')
#  www_http_1 (sdl.nodes.Software.Server.HTTP.Linux.Apache),listeningOn
+ listeningOn(8,'www_1', 'tcp', '80')
#  www_cms_1 (sdl.nodes.Software.Server.CMS.Linux.Wordpress),knows2
knows(9,A, 'venerus') <= hasUser(ID1,'www_sysuser1_1','www_1',P, R) & hasAccount(ID2,A,'www_1', 'www_sysuser1_1')
#  www_cms_1 (sdl.nodes.Software.Server.CMS.Linux.Wordpress),knows1
knows(10,A, 'venerus') <= hasUser(ID1,U,'www_1',P,'admin') & hasAccount(ID2,A,'www_1',U)
#  www_sysuser1_1 (sdl.nodes.User.Linux),hasUser
+ hasUser(11,'www_sysuser1_1', 'www_1', 'None', 'user')


## Firewall_1 ##
#  Firewall_UFW_1 (sdl.nodes.Firewall.UFW),existsRoute
+ existsRoute(12,'Server_subnet_1','Server_subnet_1','Firewall_1')
#  Firewall_UFW_1 (sdl.nodes.Firewall.UFW),existsRoute
+ existsRoute(12,'Server_subnet_1','Outside_subnet_1','Firewall_1')
#  Firewall_UFW_1 (sdl.nodes.Firewall.UFW),existsRoute
+ existsRoute(12,'Server_subnet_1','DMZ_subnet_1','Firewall_1')
#  Firewall_UFW_1 (sdl.nodes.Firewall.UFW),existsRoute
+ existsRoute(12,'Outside_subnet_1','Server_subnet_1','Firewall_1')
#  Firewall_UFW_1 (sdl.nodes.Firewall.UFW),existsRoute
+ existsRoute(12,'Outside_subnet_1','Outside_subnet_1','Firewall_1')
#  Firewall_UFW_1 (sdl.nodes.Firewall.UFW),existsRoute
+ existsRoute(12,'Outside_subnet_1','DMZ_subnet_1','Firewall_1')
#  Firewall_UFW_1 (sdl.nodes.Firewall.UFW),existsRoute
+ existsRoute(12,'DMZ_subnet_1','Server_subnet_1','Firewall_1')
#  Firewall_UFW_1 (sdl.nodes.Firewall.UFW),existsRoute
+ existsRoute(12,'DMZ_subnet_1','Outside_subnet_1','Firewall_1')
#  Firewall_UFW_1 (sdl.nodes.Firewall.UFW),existsRoute
+ existsRoute(12,'DMZ_subnet_1','DMZ_subnet_1','Firewall_1')
#  Firewall_UFW_1 (sdl.nodes.Firewall.UFW),isConnected
+ isConnected(13,'Firewall_1', 'Server_subnet_1')
#  Firewall_UFW_1 (sdl.nodes.Firewall.UFW),isConnected
+ isConnected(13,'Firewall_1', 'Outside_subnet_1')
#  Firewall_UFW_1 (sdl.nodes.Firewall.UFW),isConnected
+ isConnected(13,'Firewall_1', 'DMZ_subnet_1')
#  Firewall_UFW_1 (sdl.nodes.Firewall.UFW),isRouter
+ isRouter(14,'Firewall_1')
#  Firewall_DefaultRoute1_1 (sdl.nodes.Configuration.DefaultRoute.Firewall.UFW),existsRoute
existsRoute(15,'Outside_subnet_1', N, 'Firewall_1') <= isConnected(ID1,X, 'Outside_subnet_1') & isRouter(ID2,X) & existsRoute(ID3,'Outside_subnet_1', N, X)


## ns_1 ##
#  dns_bind_1 (sdl.nodes.Software.Server.DNS.Linux.Bind),listeningOn
+ listeningOn(16,'ns_1', 'udp', '53')
#  dns_system_1 (sdl.nodes.System.Linux),isConnected
+ isConnected(17,'ns_1', 'DMZ_subnet_1')


## db_1 ##
#  db_config_1 (sdl.nodes.Configuration.DBMS.Linux.MySQL.RootAllHosts),listeningOn
+ listeningOn(18,'db_1', 'tcp', '3306')
#  db_cmsdb_1 (sdl.nodes.Configuration.DB.Linux.MySQL),knows
knows(19,A, 'CMS') <= knows(ID1,A, 'venerus') & hasAccount(ID2,A,H,U) & hostACL(ID3,H, 'db_1', 'tcp', '3306')
#  db_system_1 (sdl.nodes.System.Linux),isConnected
+ isConnected(20,'db_1', 'Server_subnet_1')
#  db_confidentialdb_1 (sdl.nodes.Configuration.DB.Linux.MySQL),knows
knows(21,A, 'DB_confidential') <= knows(ID1,A, 'venerus') & hasAccount(ID2,A,H,U) & hostACL(ID3,H, 'db_1', 'tcp', '3306')


## root-ns_1 ##
#  root-ns_bind_1 (sdl.nodes.Software.Server.DNS.Linux.Bind),listeningOn
+ listeningOn(22,'root-ns_1', 'udp', '53')
#  root-ns_system_1 (sdl.nodes.System.Linux),isConnected
+ isConnected(23,'root-ns_1', 'Simint1_subnet_1')


## invariant_1 ##
#  invariant_1 (sdl.nodes.Invariant),existsRoute
existsRoute(24,N,M,X) <= isConnected(ID1,X,N) & isConnected(ID2,X,M) & isRouter(ID3,X)
#  invariant_1 (sdl.nodes.Invariant),hostACL1
hostACL(25,H,K,P,Q) <= listeningOn(ID1,K,P,Q) & isConnected(ID2,K,N) & isConnected(ID3,H,M) & isConnected(ID4,S,M) & isRouter(ID5,S) & existsRoute(ID6,T,N,S)
#  invariant_1 (sdl.nodes.Invariant),hostACL2
hostACL(26,H,K,P,Q) <= listeningOn(ID1,K,P,Q) & isConnected(ID2,H,N) & isConnected(ID3,K,N)
#  invariant_1 (sdl.nodes.Invariant),hasAccount
hasAccount(27,A,H,U) <= hasUser(ID1,U,H,P,R) & knows(ID2,A,U) & knows(ID3,A,P)


## client_1 ##
#  eve_1 (sdl.nodes.Principal),hasAccount
+ hasAccount(28,'eve_1', 'client_1','client_user1_1')
#  client_user1_1 (sdl.nodes.User.Linux),hasUser
+ hasUser(29,'client_user1_1', 'client_1', 'supersecret', 'admin')
#  client_system_1 (sdl.nodes.System.Linux),isConnected
+ isConnected(30,'client_1', 'Simint1_subnet_1')


## Provider_1 ##
#  Provider_Route1_1 (sdl.nodes.Configuration.Route.Firewall.VyOS),existsRoute
+ existsRoute(31,'Outside_subnet_1', 'DMZ_subnet_1','Provider_1')
#  Provider_Firewall_1 (sdl.nodes.Firewall.VyOS),existsRoute
+ existsRoute(32,'Extnet_subnet_1','Extnet_subnet_1','Provider_1')
#  Provider_Firewall_1 (sdl.nodes.Firewall.VyOS),existsRoute
+ existsRoute(32,'Extnet_subnet_1','Outside_subnet_1','Provider_1')
#  Provider_Firewall_1 (sdl.nodes.Firewall.VyOS),existsRoute
+ existsRoute(32,'Extnet_subnet_1','Simint1_subnet_1','Provider_1')
#  Provider_Firewall_1 (sdl.nodes.Firewall.VyOS),existsRoute
+ existsRoute(32,'Outside_subnet_1','Extnet_subnet_1','Provider_1')
#  Provider_Firewall_1 (sdl.nodes.Firewall.VyOS),existsRoute
+ existsRoute(32,'Outside_subnet_1','Outside_subnet_1','Provider_1')
#  Provider_Firewall_1 (sdl.nodes.Firewall.VyOS),existsRoute
+ existsRoute(32,'Outside_subnet_1','Simint1_subnet_1','Provider_1')
#  Provider_Firewall_1 (sdl.nodes.Firewall.VyOS),existsRoute
+ existsRoute(32,'Simint1_subnet_1','Extnet_subnet_1','Provider_1')
#  Provider_Firewall_1 (sdl.nodes.Firewall.VyOS),existsRoute
+ existsRoute(32,'Simint1_subnet_1','Outside_subnet_1','Provider_1')
#  Provider_Firewall_1 (sdl.nodes.Firewall.VyOS),existsRoute
+ existsRoute(32,'Simint1_subnet_1','Simint1_subnet_1','Provider_1')
#  Provider_Firewall_1 (sdl.nodes.Firewall.VyOS),isConnected
+ isConnected(33,'Provider_1', 'Extnet_subnet_1')
#  Provider_Firewall_1 (sdl.nodes.Firewall.VyOS),isConnected
+ isConnected(33,'Provider_1', 'Outside_subnet_1')
#  Provider_Firewall_1 (sdl.nodes.Firewall.VyOS),isConnected
+ isConnected(33,'Provider_1', 'Simint1_subnet_1')
#  Provider_Firewall_1 (sdl.nodes.Firewall.VyOS),isRouter
+ isRouter(34,'Provider_1')



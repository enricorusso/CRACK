runtimes = {
    'sdl.nodes.Vulnerability.Linux.RCE.Mezzanine.Werkzeug': {
        'hasAccount': '!include hasaccount-linux-werkzeug.yaml'
    },
    'sdl.nodes.Vulnerability.Linux.EOP.APT': {
        'hasAccount': '!include hasaccount-linux-eopapt.yaml'
    },
    'sdl.nodes.Vulnerability.Linux.User.RemoteEnumerable': {
        'knows': '!include knows-linux-httpenumerable.yaml '
    },
    'sdl.nodes.Vulnerability.Linux.User.RemoteWeakPassword': {
        'hasAccount': '!include hasaccount-linux-remotesshweakpass.yaml'
    },
    'sdl.nodes.Software.Server.CMS.Linux.Wordpress': {
        'knows1': '!include knows-linuxwordpress.yaml',
        'knows2': '!include knows-linuxwordpress.yaml'
    },
    'sdl.nodes.Software.Server.CMS.Linux.Mezzanine': {
        'knows1': '!include knows-linuxmezzanine.yaml',
        'knows2': '!include knows-linuxmezzanine.yaml'
    },
    'sdl.nodes.Software.Server.SSH.Linux.OpenSSH': {
        'listeningOn': '!include listeningon-linux.yaml'
    },
    'sdl.nodes.Software.Server.HTTP.Linux.Apache': {
        'listeningOn': '!include listeningon-linux.yaml'
    },
    'sdl.nodes.Software.Server.HTTP.Linux.Nginx': {
        'listeningOn': '!include listeningon-linux.yaml'
    },
    'sdl.nodes.Configuration.DBMS.Linux.MySQL.RootAllHosts': {
        'listeningOn': '!include listeningon-linux.yaml'
    },
    'sdl.nodes.Configuration.DB.Linux.MySQL': {
        'knows': '!include knows-linuxmysql.yaml'
    },
    'sdl.nodes.Invariant': {
       'hostACL1': '!include hostacl-linux.yaml',
       'hostACL2': '!include hostacl-linux.yaml',
       'existsRoute': '!include existsroute-linux.yaml'
    },
     'sdl.nodes.User.Linux': {
         'hasUser': '!include hasuser-linux.yaml'
     },
     'sdl.nodes.System.Linux': {
        'isConnected': '!include isconnected-linux.yaml'
     },
     'sdl.nodes.Firewall.UFW': {
        'isConnected': '!include isconnected-linux.yaml',
        'isRouter': '!include isrouter-linux.yaml',
        'existsRoute': '!include existsroute-linux.yaml'
     },
     'sdl.nodes.Firewall.VyOS': {
        'isConnected': '!include isconnected-vyos.yaml',
        'isRouter': '!include isrouter-linux.yaml',
        'existsRoute': '!include existsroute-linux.yaml'
     },
     'sdl.nodes.Configuration.Route.Firewall.VyOS': {
         'existsRoute': '!include existsroute-linux.yaml'
     },
     'sdl.nodes.Configuration.DefaultRoute.Firewall.UFW': {
         'existsRoute': '!include existsroute-linux.yaml'
     },
}
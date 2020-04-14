#python snmp trap receiver
from pysnmp.entity import engine, config
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv
#from pysnmp.proto import rfc1902
#from pysnmp.proto.api import v2c
import os,sys
from datetime import datetime
from clases import clase_config

OID_reference = {
    '1.3.6.1.6.3.1.1.5.0':'hwLoadAndBackupTrapsOID',
    '1.3.6.1.6.3.1.1.5.1':'coldStart',
    '1.3.6.1.6.3.1.1.5.2':'warmStart',
    '1.3.6.1.6.3.1.1.5.3':'linkDown',
    '1.3.6.1.6.3.1.1.5.4':'linkUp',
    '1.3.6.1.6.3.1.1.5.5':'authenticationFailure',
    '1.3.6.1.6.3.1.1.5.6':'egpNeighborLoss',
    '1.3.6.1.2.1.1.3.0': 'sysUpTimeInstance',
    '1.3.6.1.6.3.1.1.4.1.0':'snmpTrapOID',
    '1.3.6.1.6.3.18.1.3.0':'snmpTrapAddress',
    '1.3.6.1.6.3.18.1.4.0':'snmpTrapCommunity',
    '1.3.6.1.6.3.1.1.4.3.0':'snmpTrapEnterprise',
    '1.3.6.1.2.1.1.1.0':'sysDescr'
}


# Create SNMP engine with autogenernated engineID and pre-bound
# to socket transport dispatcher
snmpEngine = engine.SnmpEngine()

# Transport setup
TrapAgentAddress='127.0.0.1'; #Trap listerner address
Port=162;  #trap listerner port

print('\n{} Iniciando Auto_SNMPTrapReceiver'.format(datetime.now()));

try:
    # UDP over IPv4, first listening interface/port
    config.addTransport(
        snmpEngine,
        udp.domainName + (1,),
        udp.UdpTransport().openServerMode((TrapAgentAddress, Port))
    )

	# configuracion=clase_config.config('config.ini')
	# items=configuracion.ShowItemSection('TRANSPORT_SETUP')
	# print (items)
	# items=configuracion.ShowItemSection('TRANSPORT_SETUP')
	# print (items)
	# print (configuracion.ShowValueItem('TESTING','DB_NAME'))
	# configuracion.change('TESTING','DB_NAME','Peloncho')
	# print (configuracion.ShowValueItem('TESTING','DB_NAME'))
	# configuracion.write()

except Exception as err:
    print("Error: {}".format(err))
else: 
    print('--------------------------------------------------------------------------');
    print('Start SNMPTrapReceiver -> {}'.format(datetime.now()));
    print("Agent is listening SNMP Trap on "+TrapAgentAddress+" , Port : " +str(Port));
    print('--------------------------------------------------------------------------');
    
    # SNMPv1/2c setup
    config.addV1System(snmpEngine, 'my-area', 'public')

    # Callback function for receiving notifications
    # noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
    def cbFun(snmpEngine, stateReference, contextEngineId, contextName,
          varBinds, cbCtx):
        print('{} : Received new Trap message'.format(datetime.now()));
        print('{} : Notification from ContextEngineId: {}, ContextName: {}'.format(datetime.now(),contextEngineId.prettyPrint(),
                                                                        contextName.prettyPrint()))
        for name, val in varBinds:
            name_OID=name.prettyPrint()
            value_OID=val.prettyPrint()    
            if (OID_reference.get(name.prettyPrint())!=None):
                name_OID=OID_reference.get(name.prettyPrint())
            if (OID_reference.get(val.prettyPrint())!=None):
                value_OID=OID_reference.get(val.prettyPrint())
            
            print('{} : Name: {} | Val: {}'.format(datetime.now(),name_OID,value_OID))

        print('--------------------------------------------------------------------------');

    # Register SNMP Application at the SNMP engine
    ntfrcv.NotificationReceiver(snmpEngine, cbFun)

    # this job would never finish
    snmpEngine.transportDispatcher.jobStarted(1)  

    # Run I/O dispatcher which would receive queries and send confirmations
    try:
        snmpEngine.transportDispatcher.runDispatcher()
    except:
        snmpEngine.transportDispatcher.closeDispatcher()

finally:
    print('{} : Finaliza app Auto_SNMPTrapReceiver'.format(datetime.now()))

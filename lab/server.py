from http import server
from opcua import Server,ua 
from opcua.server.user_manager import UserManager
import datetime
import time
import control.config as config

obj_list = []
var_list = []
value_list = []
id = 'ns=2;s=V'
power_value = True

# user manager
def user_manager(isession, username, password):
    print(isession, username, password)
    isession.user = UserManager.User
    return username in config.users_db and password == config.users_db[username]

def start_server(stateMachine, count):
    global power_value
    TARGET = stateMachine[0].target
    POWER = stateMachine[0].power
    server = Server()
    server.set_endpoint(config.URL)

    # load server certificate and private key. This enables endpoints
    # with signing and encryption.
    # server.load_certificate("certificate-example.der")
    # server.load_private_key("private-key-example.pem")

    # set all possible endpoint policies for clients to connect through
    server.set_security_policy([
        ua.SecurityPolicyType.NoSecurity,
        # ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
        # ua.SecurityPolicyType.Basic256Sha256_Sign,
    ])

    # set the security endpoints for identification of clients
    server.set_security_IDs(["Username"])

    # set the user_manager function
    server.user_manager.set_user_manager(user_manager)
    node =  server.get_objects_node()
    custom_obj_type = node.add_object_type(id, "Thermostats")

    therm_id = custom_obj_type.add_variable(0, "Id", '')
    therm_id.set_modelling_rule(True)
    temp = custom_obj_type.add_variable(1, "Temperature", 0.0)
    temp.set_modelling_rule(True)
    state = custom_obj_type.add_variable(2, "State", '')
    state.set_modelling_rule(True)
    temp_max = custom_obj_type.add_variable(3, "Temperature_max", 0.0)
    temp_max.set_modelling_rule(True)
    temp_min = custom_obj_type.add_variable(4, "Temperature_min", 0.0)
    temp_min.set_modelling_rule(True)
    target = custom_obj_type.add_variable(5, "Target", 0)
    target.set_modelling_rule(True)
    target.set_writable()
    target = custom_obj_type.add_variable(6, "Power", 0)
    target.set_modelling_rule(True)
    target.set_writable()

    for l in range(count):
        myobj = node.add_object(id+'{}'.format(str(l+1)), "Therm{}".format(l+1), custom_obj_type.nodeid)
        obj_list.append(myobj)

    var_list = add_variables(count, stateMachine, obj_list)

    server.start()
    print("Server started at {}".format(config.URL))

    for n in range(int(count)):
    #     var_list[n].target.set_value(TARGET)
        var_list[n].power.set_value(POWER)

    while True:
        for i in range(count):
            ID = stateMachine[i].id
            TEMP = stateMachine[i].temp
            STATE = stateMachine[i].state
            TEMP_MAX = stateMachine[i].temp_max
            TEMP_MIN = stateMachine[i].temp_min
            TARGET = var_list[i].target.get_value() 
            # stateMachine[i].target = TARGET
            TARGET = stateMachine[i].target
            POWER = var_list[i].power.get_value() 
            stateMachine[i].power = POWER

            print("Server: "+str(ID), str(TEMP), str(STATE), str(TARGET))

            var_list[i].therm_id.set_value(ID)
            var_list[i].temp.set_value(TEMP)
            var_list[i].state.set_value(STATE)
            var_list[i].temp_max.set_value(TEMP_MAX)
            var_list[i].temp_min.set_value(TEMP_MIN)
            # Random target change
            var_list[i].target.set_value(TARGET)

        time.sleep(config.server_refresh)
    
class therm_var:
    def __init__(self):
        self.therm_id = 0
        self.temp = 0
        self.time_value = 0
        self.state = 0
        self.temp_max = 0
        self.temp_min = 0
        self.target = 0
        self.power = 0

def add_variables(count, stateMachine, obj_list):
    list = []
    for j in range(count):
        therm_variables = therm_var()
        therm_variables.therm_id = obj_list[j].get_child(["0:Id"])
        therm_variables.temp = obj_list[j].get_child(["1:Temperature"])
        therm_variables.state = obj_list[j].get_child(["2:State"])
        therm_variables.temp_max = obj_list[j].get_child(["3:Temperature_max"])
        therm_variables.temp_min = obj_list[j].get_child(["4:Temperature_min"])
        therm_variables.target = obj_list[j].get_child(["5:Target"])
        therm_variables.power = obj_list[j].get_child(["6:Power"])
        list.append(therm_variables)   
    return list
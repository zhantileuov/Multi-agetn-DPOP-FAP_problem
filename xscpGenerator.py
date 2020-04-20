import xml.etree.ElementTree as ET

base_addr = "FullRLFAP/CELAR"
dataset="50"
instance = ET.Element('instance')
presentation = ET.SubElement(instance, 'presentation')
presentation.set('name','example_prob1')
presentation.set('maxConstraintArity','2')
presentation.set('maximize','false')
presentation.set('format','XCSP 2.1_FRODO')
agents = ET.SubElement(instance, 'agents')
nbAgents = 0
for line in open(base_addr+"/"+dataset+"/var.txt", "r"):
    print('X'+str(line[0:3]).strip())
    agent = ET.SubElement(agents, 'agent')
    agent.set('name','X'+str(line[0:3]).strip())
    nbAgents += 1
agents.set('nbAgents',str(nbAgents))
domains = ET.SubElement(instance, 'domains')
nbDomains = 0
for line in open(base_addr+"/"+dataset+"/dom.txt", "r"):
    domain_str=line[7:]
    domain = ET.SubElement(domains, 'domain')
    domain.set('name', 'DOM'+str(line[0:3]).strip())
    nbValues = str(line[4:7]).strip()
    #nbValues = len(list(filter(None,((domain_str.rstrip(" ")).split(' ')))))
    domain.set('nbValues', str(nbValues))
    domain.text = domain_str
    nbDomains += 1

domains.set('nbDomains',str(nbDomains))
len(list(filter(None,((domain_str.rstrip(" ")).split(' ')))))
variables = ET.SubElement(instance, 'variables')
variables.set('nbVariables',str(nbAgents))
for line in open(base_addr+'/'+dataset+"/var.txt", "r"):
    print(line[0:3])
    variable = ET.SubElement(variables, 'variable')
    variable.set('name','X'+str(line[0:3]).strip())
    variable.set('domain','DOM'+str(line[4:7]).strip())
    variable.set('agent','X'+str(line[0:3]).strip())

#function
functions = ET.SubElement(instance, 'functions')
nbFunctions = 2
functions.set('nbFunctions',str(nbFunctions))
#function greaterthan
function1 = ET.SubElement(functions, 'predicate')
function1.set('name','GRT')
function1.set('return','int')
parameters = ET.SubElement(function1,'parameters')
parameters.text = 'int X1 int X2 int D'

expression = ET.SubElement(function1, 'expression')

functional = ET.SubElement(expression, 'functional')
functional.text = 'if(gt(abs(sub(X1, X2)), D), abs(sub(abs(sub(X1, X2)), D)), mul(3, abs(sub(abs(sub(X1, X2)), D))))'

#function equal
function2 = ET.SubElement(functions, 'predicate')
function2.set('name','EQL')
function2.set('return','int')

parameters = ET.SubElement(function2,'parameters')
parameters.text = 'int X1 int X2 int D'

expression = ET.SubElement(function2, 'expression')

functional = ET.SubElement(expression, 'functional')
functional.text = 'if(eq(abs(sub(X1, X2)), D), 0, abs(sub(abs(sub(X1, X2)), D))'

#constraint
constraints = ET.SubElement(instance, 'constraints')
nbConstraints = 0
for line in open(base_addr+'/'+dataset+"/ctr.txt", "r"):
    print(line[12:15])
    #print(line[10:11])
    constraint = ET.SubElement(constraints, 'constraint' )
    constraint.set('name','constraint NUM'+str(nbConstraints))
    constraint.set('arity',str(2))
    constraint.set('scope','X'+str(line[0:3]).strip()+' X'+str(line[4:7]).strip())
    if line[10:11] == '=':
        constraint.set('reference',"EQL")
    else:
        constraint.set('reference',"GRT")

    parameters = ET.SubElement(constraint,'parameters')
    parameters.text = 'X'+str(line[0:3]).strip()+' X'+str(line[4:7]).strip()+' '+str(line[12:15]).strip()
    nbConstraints += 1
constraints.set('nbConstraints',str(nbConstraints))

mydata = ET.tostring(instance)
myfile = open("Eldi"+dataset+".xml", "w")
myfile.write(mydata.decode('utf-8'))
myfile.close()

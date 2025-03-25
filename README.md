# Sp3llsWizard
This repository contains the implementation and experimental toolbench presented in the paper “From Sound Workflow Nets to LTLf Declarative Specifications by Casting Three Spells". This work introduces a systematic approach to synthesize declarative process specifications from safe and sound Workflow nets, ensuring that the original behavior is fully preserved. Here, you'll find the complete toolchain and experimental setups, tested on both synthetic and real-world datasets, analyzing the correctness and performance of our implemented algorithm. 

## Overview
Sp3llsWizard is an approach designed to formally synthesize DECLARE specifications from sound Workflow nets. The proof-of-concept implememtation automatically generates LTLf constraints from an input Workflow net in the form of a .pnml file.

## Repository

The main content of the repository is structured as follows:
-  [/src/](https://github.com/l2brb/Sp3llsWizard/tree/main/src): the root folder of the implementation source code
    -  [/src/declare-translator](https://github.com/l2brb/Sp3llsWizard/tree/main/src/declare-translator): contains the algorithm's implementation
-  [/evaluation/](https://github.com/l2brb/Sp3llsWizard/tree/main/evaluation): folder containing datasets and results of our tests
    - [/evaluation/bisimualtion/](https://github.com/l2brb/Sp3llsWizard/tree/main/evaluation/bisimulation) contains the convergence test data 
    - [/evaluation/setcardinality/](https://github.com/l2brb/Sp3llsWizard/tree/main/evaluation/d_contraints) includes the memory usage tests data 
    - [/evaluation/formulasize/](https://github.com/l2brb/Sp3llsWizard/tree/main/evaluation/n_constraints) contains the data of the scalability tests
    - [/evaluation/realworld/](https://github.com/l2brb/Sp3llsWizard/tree/main/evaluation/realworld) contains the data of the scalability tests
-  [/diagnostics/](https://github.com/l2brb/Sp3llsWizard/tree/main/evaluation/conformance): folder containing datasets and results of our tests

## Setup
As a requirement, python 3.13.0 at least should be installed on your machine. To launch the .sh test files, you have to run them on a Unix-based system with a BASH shell. No installation procedure is required. This version has been tested on both a Ubuntu Linux (24.04.1) and a Mac OS X machine.


## Evaluation
We evaluated our algorithm on a range of both synthetic and real-world data. For the real-world testbed, we take as input processes discovered by a well-known imperative process mining algorithm from a collection of openly available event logs. We conducted the performance tests on an AMD Ryzen 9 8945HS CPU at 4.00 GHz with 32 GB RAM running Ubuntu 24.04.1. 


#### Bisimulation

To experimentally validate the correctness of our approach in the transmission and computation phases, we run a [bisimualtion](https://github.com/l2brb/Sp3llsWizard/tree/main/evaluation/bisimulation) test. To this end, we . We run the stand-alone MINERful... . The convergence results are available in [/output/](https://github.com/l2brb/Sp3llsWizard/tree/main/evaluation/bisimulation) in the form of a workflow net.

### Performance analysis

To evaluate the runtime memory utilization of our Sp3llsWizard implementation, we run a [performance](https://github.com/l2brb/Sp3llsWizard/tree/main/evaluation/d_contraints) test, split into two different configurations.


#### Increasing constraint-set cardinality.
![sampleWN](/evaluation/performance/n_constraints/expanded_pnml/images/rsample.png)
![expantionrules](/evaluation/performance/n_constraints/expanded_pnml/images/cardinality.png)



#### Increasing constraint formula size
![conditionalexpantion](/evaluation/performance/n_constraints/expanded_pnml/images/rconditional.png)



#### Real-world process model testing. 



### Process Diagnostics









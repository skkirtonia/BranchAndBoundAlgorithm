# Branch and Bound Algorithm
Implemented Branch and Bound Algorithm with various approaches for variable selection and node selection. <br/>
**Variable selection approaches**<br/>
* Most fractional
* Least fractional
* First variable
* Last variable <br/>

**Node selection approaches**<br/>
* Depth first
* Breadth first
* Best first

The MILP model is converted to the following form of LP relaxation:<br/>
$min$ or $max$ &emsp; $c^Tx$ <br/>
$s.t.$ &emsp;&emsp; &emsp; &nbsp; $A_{ub}x \leq b_{ub}$  <br/>
&emsp;&emsp; &emsp; &emsp;&emsp; $A_{eq}x = b_{eq}$  <br/>
&emsp;&emsp; &emsp; &emsp;&emsp; $lb \leq x \leq ub$  <br/>
An argument *int_var_indicator* which is a binary list is provided to indicate which variables should take the integer values. <br/>
The class **BnB.py** takes all inputs to solve the MILP problem using Branch and Bound Algorithm.<br/>
Sample inputs are used to solve some example MILP problems in python scripts DataMIP.py and Solve.py.

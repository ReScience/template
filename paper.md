---
title: "Interaction between cognitive and motor cortico-basal
        ganglia loops during decision making: a computational study"
author:
  - name: Meropi Topalidou
    affiliation: 1, 2, 3
  - name: Nicolas P. Rougier
    affiliation: 1, 2, 3
address:
  - code:    1
    address: INRIA Bordeaux Sud-Ouest, Bordeaux, France.
  - code:    2
    address: LaBRI, Université de Bordeaux, Institut Polytechnique de Bordeaux,
             Centre National de la Recherche Scientifique, UMR 5800, Talence, France.
  - code:    3
    address: Institut des Maladies Neurodégénératives, Université  de Bordeaux,
             Centre National de la Recherche Scientifique, UMR 5293, Bordeaux, France.
contact:
  - Nicolas.Rougier@inria.fr
editor:
  - Editor name
reviewer:
  - Reviewer name
  - Reviewer name
publication:
  received:  May,  1, 2015
  accepted:  June, 1, 2015
  published: July, 1, 2015
  volume: "**1**"
  issue: "**1**"
  date: May 2015
repository:
  article:  "http://github.com/rescience/rescience/wiki"
  code:     "http://github.com/rescience/rescience/wiki"
  data:
  notebook: "http://github.com/rescience/rescience/wiki"
reproduction:
  - "*Interaction between cognitive and motor cortico-basal ganglia loops during decision making: a computational study*, M. Guthrie, A. Leblois, A. Garenne, and T. Boraud, Journal of Neurophysiology, 109, 2013."
bibliography: paper.bib
---

# Introduction

We propose a reference implementation of [@guthrie:2013] that introduces an
action selection mechanism in cortico-basal ganglia loops based on a
competition between the positive feedback, direct pathway through the striatum
and the negative feedback, hyperdirect pathway through the subthalamic nucleus.

# Methods

The reference implementation has been coded in python using DANA
[@rougier:DANA] which is a python framework for distributed, asynchronous,
numerical and adaptive computing. The model fits the DANA paradigm and makes
the source code easily understandable. We provide below the formal description
of the model according to the proposition of Nordlie et al. [@nordlie:2009]
for reproducible descriptions of neuronal network models.

Table              Description
------------------ ------------------------------------------------------------------
Populations        Cortex (motor, associative & cognitive),
                   Striatum (motor, associative & cognitive),
                   GPi (motor & cognitive),
                   STN (motor & cognitive),
                   Thalamus (motor & cognitive)
Topology           --
Connectivity       One to one, one to many (divergent), many to one (convergent)
Neuron model       Dynamic rate model
Channel model      --
Synapse model      Linear synapse
Plasticity         Reinforcement learning rule
Input              External current in cortical areas (motor, associative & cognitive)
Measurements       Firing rate
------------------ -------------------------------------------------------------------

Table: Model description following [@nordlie:2009] prescription.


Name                 Elements          Size           Threshold Noise Initial state
-------------------- ----------------- -------------- --------- ----- -------------
Cortex motor         Linear neuron     $1 \times 4$   -3        1.0%  0.0
Cortex cognitive     Linear neuron     $4 \times 1$   -3        1.0%  0.0
Cortex associative   Linear neuron     $4 \times 4$   -3        1.0%  0.0
Striatum motor       Sigmoidal neuron  $1 \times 4$   0         0.1%  0.0
Striatum cognitive   Sigmoidal neuron  $4 \times 1$   0         0.1%  0.0
Striatum associative Sigmoidal neuron  $4 \times 4$   0         0.1%  0.0
GPi motor            Linear neuron     $1 \times 4$   +10       3.0%  0.0
GPi cognitive        Linear neuron     $4 \times 1$   +10       3.0%  0.0
STN motor            Linear neuron     $1 \times 4$   -10       0.1%  0.0
STN cognitive        Linear neuron     $4 \times 1$   -10       0.1%  0.0
Thalamus motor       Linear neuron     $1 \times 4$   -40       0.1%  0.0
Thalamus cognitive   Linear neuron     $4 \times 1$   -40       0.1%  0.0
Values ($V_i$)       Scalar            $4$            --        --    0.5
-------------------- ----------------- -------------- --------- ----- -------------

Table: Populations


Source               Target               Pattern                   Weight  Gain  Plastic
-------------------- -------------------- ------------------------- ------- ----- -------
Cortex motor         Thalamus motor       $(1,i) \rightarrow (1,i)$ 1.0     0.4   No 
Cortex cognitive     Thalamus cognitive   $(i,1) \rightarrow (i,1)$ 1.0     0.4   No 
Cortex motor         STN motor            $(1,i) \rightarrow (1,i)$ 1.0     1.0   No 
Cortex cognitive     STN cognitive        $(i,1) \rightarrow (i,1)$ 1.0     1.0   No 
Cortex motor         Striatum motor       $(1,i) \rightarrow (1,i)$ 0.5     1.0   No
Cortex cognitive     Striatum cognitive   $(i,1) \rightarrow (i,1)$ 0.5     1.0   Yes
Cortex motor         Striatum associative $(1,i) \rightarrow (.,i)$ 0.5     0.2   No
Cortex cognitive     Striatum associative $(i,1) \rightarrow (i,.)$ 0.5     0.2   No
Cortex associative   Striatum associative $(i,j) \rightarrow (i,j)$ 0.5     1.0   No
Thalamus motor       Cortex motor         $(1,i) \rightarrow (1,i)$ 1.0     1.0   No
Thalamus cognitive   Cortex cognitive     $(i,1) \rightarrow (i,1)$ 1.0     1.0   No
GPi motor            Thalamus motor       $(1,i) \rightarrow (1,i)$ 1.0     -0.5  No
GPi cognitive        Thalamus cognitive   $(i,1) \rightarrow (i,1)$ 1.0     -0.5  No
STN motor            GPi motor            $(1,i) \rightarrow (1,i)$ 1.0     1.0   No
STN cognitive        GPi cognitive        $(i,1) \rightarrow (i,1)$ 1.0     1.0   No
Striatum cognitive   GPi cognitive        $(i,1) \rightarrow (i,1)$ 1.0     -2.0  No
Striatum motor       GPi motor            $(i,1) \rightarrow (i,1)$ 1.0     -2.0  No
Striatum associative GPi motor            $(.,i) \rightarrow (1,i)$ 1.0     -2.0  No
Striatum associative GPi cognitive        $(i,.) \rightarrow (i,1)$ 1.0     -2.0  No
-------------------- -------------------- ------------------------- ------- ----- -------

Table: Connectivity


Linear neuron
------------------ -----------------------------------------
Type               Rate model
Membrane Potential $\tau dV/dt = -V + I_{syn} + I_{ext} - h$
                   $U = max(V,0)$
------------------ -----------------------------------------

Table: Neuron Model (1)


Sigmoidal neuron
------------------ --------------------------------------------------------------------------
Type               Rate model
Membrane Potential $\tau dV/dt = -V + I_{syn} + I_{ext} - h$
                   $U = V_{min} - (V_{max}-V_{min}) / \left(1+e^{\frac{V_h - V}{V_c}}\right)$
------------------ --------------------------------------------------------------------------

Table: Neuron Model (2)


Linear synapse
-------------- -----------------------------------------------------------------------------------
Type           Weighted sum
Output         $I^{B}_{syn} = \sum_{A \in sources}(G_{A \rightarrow B} W_{A \rightarrow B} U_{A})$
-------------- -----------------------------------------------------------------------------------

Table: Synapse


Reinforcement learning
---------------------- --------------------------------------------------------------------
Type                   Delta rule
Delta                  $\Delta W_{A \rightarrow B} = \alpha \times PE \times U_{B}$
                       $PE = Reward - V_{i}$
                       $\alpha = 0.01$ if $PE < 0$ (LTD), $\alpha = 0.02$ if $PE > 0$ (LTP)
---------------------- --------------------------------------------------------------------

Table: Plasticity


# Results

We did not reproduce all analysis of the original article but concentrate our
efforts on the main results which are illustrated on figures 4 & 5 in the
original article [@guthrie:2013]. Figure 1 illustrates the decision dynamic
while figure 3 shows model performances on the task.

![**Activity in the cortical population during a single trial of action selection.**
  This is the reproduction of figure 4 of the original article. The overall shape is
  slightly different because of the noise that makes the cognitive and motor decision
  to reach threshold at different times. The oscillations between time t=0 and time
  t=500ms are characteristic of the model. All activities have been recorded before
  any learning occurs in the model.](code/figure-1.pdf)

![**Activity in all populations during a single trial of action selection.**
  This specific figure was not included in the original article but has been
  proved to be very useful when debuggin the model. All activities have been
  recorded before any learning occurs in the model.](code/figure-2.pdf)

# Conclusion

We were able to reproduce original results, confirming the correctness of the
original implementation of the model.


# References

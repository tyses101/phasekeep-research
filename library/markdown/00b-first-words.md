# First Words

*A starting glossary of every background word, for a reader who knows nothing yet*


## Read this before anything else

This page assumes you know **nothing** about light, quantum physics or computing. Every word the library leans on is explained here in plain language, in the order a newcomer needs it. Nothing is skipped because it seems obvious. You do not need to memorize any of it. Come back whenever a word stops making sense.

Two things to know first:

- The words in **bold** are the ones used later in the volumes. Where a word has a nickname or symbol, it is given.
- The full project glossary at the back ([Appendix 1](A1-glossary.md)) lists PhaseKeep's own terms. This page covers the background words those terms are built from.

>
> **Key idea**
> **The whole project in six lines.** Light comes in tiny pieces called photons. A photon has several properties, such as which way it wiggles and how its beam twists. PhaseKeep proposes using two of those properties together so that one photon carries one of four labels. Ordinary optical parts can then change the label. A separate check decides whether the change worked. Every number in the library says how much we know about it and how we know it.


## 1. Everyday words used in a special way

- **Information**: a choice between possibilities. Which of two switches is on, or which of four labels a photon carries.
- **Bit**: the smallest piece of information, a choice between two things, written 0 or 1.
- **State**: a full description of how something is set up right now. "The photon's state" means everything about it that we could in principle find out.
- **System**: whatever we are describing. A photon, a register or a memory.
- **Model**: a set of rules and numbers, usually run on a computer, that imitates how something behaves. A model is only as good as the numbers put into it.
- **Simulation**: running a model to see what it predicts. A simulation is not an experiment.
- **Assumption**: a number or fact we chose instead of measuring.
- **Measurement (in the lab)**: reading a value from real equipment. Every PhaseKeep number so far is a calculation or a simulation, **not** a lab measurement.
- **Classical**: ordinary, non-quantum. A classical computer works with bits that are definitely 0 or 1.
- **Resource**: anything that is used up or costs something, such as the number of optical parts, the amount of light that survives, or the time taken.

## 2. Light

- **Light**: a wave of electric and magnetic fields that carries energy. It can also be treated as a stream of particles (see photon).
- **Wave**: a pattern that repeats as it travels, with crests and troughs, like a ripple on a pond.
- **Wavelength**: the distance between two neighbouring crests. It sets the colour of the light.
- **Photon**: the smallest piece of light. One photon cannot be split into halves. Single photons are used because quantum effects are easiest to see when you handle one at a time.
- **Bright light, or classical light**: a beam with a huge number of photons, such as a laser pointer. It behaves like a smooth wave. Many tests are done with bright light first because it is easier to handle than single photons.
- **Beam**: light travelling in a narrow stream.
- **Laser**: a source of very pure, steady, single-colour light.
- **Amplitude of a wave**: how tall the waves are. A bigger amplitude means a brighter beam. (Quantum amplitudes in section 3 are a related but different idea.)
- **Phase**: where in its up-and-down cycle a wave is. Two waves can be the same size but shifted, and that shift is a phase difference.
- **Interference**: what happens when two waves overlap. Where crests meet crests the light gets brighter (**constructive** interference). Where a crest meets a trough it cancels (**destructive** interference). Much of what follows depends on this.
- **Polarization**: the direction in which the light's electric field wiggles, such as up and down or side to side. Polarized sunglasses use it. **H** means horizontal, **V** means vertical. There are also diagonal and circular kinds. In circular polarization the wiggle direction turns steadily as the light moves.
- **Wavefront**: an imaginary surface joining the crests of a wave. In an ordinary beam it is flat. Picture a sheet moving forward.
- **Orbital angular momentum, OAM, or "twist"**: some beams have a wavefront that spirals like a corkscrew or a spiral staircase as it travels. The number of turns is a whole number, called the twist, written ℓ (the letter ell). The value 0 is an ordinary beam. A beam with ℓ of +1 spirals one way and −1 spirals the other. A twisted beam has a dark spot in the middle, so it looks like a ring or doughnut.
- **Mode**: one particular allowed shape of a beam. "The ℓ = +1 mode" means the beam shape with one turn of twist. Think of modes as separate lanes the light can use.
- **Optical part, or component**: any physical piece that handles light. It is not a computer part.
- **Mirror**: reflects light. It reverses the direction of a twist, so ℓ = +1 becomes ℓ = −1.
- **Beam splitter**: a part that sends part of a beam one way and the rest another way.
- **Polarizing beam splitter**: a beam splitter that sorts light by polarization, for example sending H straight on and V off to the side.
- **Waveplate**: a slab of crystal that changes the polarization of light passing through it. A **half-wave plate**, set at the right angle, can turn H into V. A **quarter-wave plate** turns straight-line polarization into circular and back.
- **Spatial light modulator**: a screen-like device that can reshape a beam, including adding a twist.
- **Detector**: a device that notices light. A **single-photon detector** responds to one photon, usually with a click.
- **Loss**: light that is absorbed, scattered or sent somewhere we cannot use. Loss is the main enemy in this project.

## 3. Quantum words

These are the words people find hardest. Take them slowly. Nothing in the library needs more than this.

- **Quantum**: the rules that govern very small things, such as photons, atoms and electrons. They differ from everyday experience in the ways below.
- **State (quantum)**: the full description of a photon's properties. A photon's state can be a definite property, such as "horizontal", or a mixture.
- **Basis state**: one of a chosen set of clearly different states that can be told apart perfectly. Horizontal and vertical polarization are two basis states.
- **Superposition**: a state that is a blend of basis states, not one or the other. It does **not** mean the photon is secretly one of them and we do not know which. A diagonal polarization is a superposition of H and V.
- **Amplitude (quantum)**: a number, which can be positive, negative or complex, that says how much of each basis state is in a blend. The chance of seeing an outcome is the **size of its amplitude, squared**.
- **Probability**: the chance of an outcome. Probabilities of all possible outcomes add up to 1 (or 100 %).
- **Relative phase**: the shift between two parts of a blend. Two blends can give exactly the same probabilities and still differ in relative phase, and that difference can change what later operations do. It is the most easily lost piece of information.
- **Measurement**: asking a quantum system a question and getting an answer. A measurement gives one outcome and usually changes the state, so the original blend is gone. Reading a state is therefore not the same as copying it.
- **Coherence**: the property of keeping a definite relative phase between parts of a blend. Losing it is called decoherence. A memory or a beam path is good if it preserves coherence.
- **Qubit**: a quantum system with two basis states. The quantum version of a bit.
- **Qudit**: a quantum system with *d* basis states. A system with four is a four-level system, sometimes called a ququart.
- **Dimension**: the number of basis states. A qubit has dimension 2 and the Tetragon has dimension 4.
- **Entanglement**: a link between two separate things such that the pair has a state that cannot be written as a separate state for each one.
- **High-dimensional entanglement**: entanglement between systems that each have more than two levels. Two entangled four-level systems, for example, have 16 joint states.
- **Ebit**: the unit of entanglement. One ebit is the entanglement of one maximally entangled pair of two-level systems. Two maximally entangled four-level systems hold 2 ebits, because the count for equal weights is the base-2 logarithm of the number of levels.
- **Hyperentanglement**: entanglement in more than one property of the same two photons at once, such as polarization and twist.
- **Separable and non-separable**: a joint state is **separable** if it can be written as one state for the first property times one state for the second. If not, it is **non-separable**. We use these words for two properties of **one** photon. The word entangled is used for two *separate* photons.
- **Schmidt weights**: two numbers that tell you how separable a two-part state is. Weights of 1 and 0 mean fully separable. Weights of 0.5 and 0.5 mean the most non-separable a two-level pair can be.
- **Fidelity**: a score from 0 to 1 (0 % to 100 %) for how close a state is to the one we wanted. 1 is perfect. Fidelity says nothing about how much light survived. That is a separate number.
- **Reversible, or unitary**: an operation that loses no information, so it can in principle be run backwards. All the "perfect" operations in the math are unitary. Filtering and measuring are **not**.
- **No-cloning**: an unknown quantum state cannot be copied exactly. A recipe that you know can be repeated. A state that you do not know cannot be duplicated.
- **Photon number**: how many photons are in a mode. The **vacuum** means none.
- **Noise photons, or thermal photons**: unwanted photons that arrive in a mode and spoil the state. The average number of them is written n̄ (n-bar) later on.

## 4. Words for how PhaseKeep encodes information

- **Encoding**: choosing which physical property stands for which label.
- **Encoding Axis (EA, plural Axies)**: one physical property chosen to carry part of a label, such as polarization or twist. "Axis" because, like a map axis, it has a set of distinguishable values along it.
- **Address**: the label of one basis state. On the Tetragon the addresses are 00, 01, 10 and 11.
- **Register**: an information-carrying system with a defined set of states, such as the group of photon properties that together hold one address.
- **Tetragon (PK-Q4)**: our four-address register, made from one photon and two properties. The first digit of an address is the polarization (0 means H, 1 means V). The second digit is the twist (0 means ℓ = −1, 1 means ℓ = +1). So 00 is H with twist −1, 01 is H with twist +1, 10 is V with twist −1 and 11 is V with twist +1.
- **Geometric Encoding Axies (GEA)**: drawing the addresses as the corners of a shape. Two binary properties give a square, three give a cube, and more give a hypercube. Changing one property moves you along one edge.
- **Corner, or vertex**: one address on the shape.
- **Edge, or line**: two corners that differ in one property only, for example 00 and 01.
- **Diagonal**: two corners that differ in two properties, for example 00 and 11.
- **Face**: a flat piece of the shape, such as a square within a cube.
- **Hypercube**: the same shape in more than three dimensions. You cannot picture it, but you can count its corners, edges and faces by formula.
- **Subspace**: the set of states you can build out of a chosen few addresses. An edge gives a two-address subspace and a square gives a four-address one.
- **Edge blend and diagonal blend**: a mix of two corners joined by an edge, or by a diagonal. The diagonal kind is non-separable. The edge kind is not.

## 5. Words for changing and checking

- **Operation, or gate**: a step that changes a state. In optics it is made by a part such as a waveplate or a mirror.
- **Controlled Transformation (CT)**: a physical operation that we can set and repeat that changes the encoded information. "Controlled" means we can adjust it, not that it depends on another photon.
- **Conditional operation, or controlled gate**: an operation that happens only if another system is in a certain state. Making this work between two photons is hard, because photons ignore each other.
- **Closure**: whether an operation keeps the photon inside the set of states we are using. An operation that sends it to some other state is not closed on our set.
- **Ancilla, or helper photon**: an extra photon, not part of the answer, that is used to make an operation work or to check that it worked.
- **Herald, or heralded**: a detector click that is *supposed* to announce that an operation succeeded. **Heralded** means success is announced this way. Detection is not the same as verification, because the click can fire when the output is actually wrong.
- **Post-selection**: keeping only the runs where a chosen detector outcome occurred, and throwing the rest away. It makes results look better than the success rate really is, so the discarded runs have to be counted.
- **Success probability, or yield**: the fraction of attempts that work. For a probabilistic operation this can be small, such as 1 in 8.
- **Buddy System**: the PhaseKeep idea of preparing helper photons and checking each operation before going on.
- **Buddy Check**: a test with three honest answers. **PASS** means there is demonstrated evidence it worked. **FAIL** means there is demonstrated evidence it did not. **UNKNOWN** means we cannot tell, and that is the default.
- **Certification, or verification**: proving that a state or result is what we think it is, ideally without using up the photons.
- **Compiler, or controller**: a classical program that decides which supported operations to apply and in what order. It is ordinary software.

## 6. Words for memory and loss

- **Quantum memory**: a device that stores a photon's state and gives it back later. Keeping the relative phase is the hard part.
- **Atomic vapor, or vapour, memory**: a memory built from a cell of atomic gas. Light is absorbed into the atoms and later released.
- **Transmission, or efficiency**: the fraction of light that comes through a part or a whole chain. 98 % means 2 % was lost. Losses along a chain **multiply**.
- **Survival**: the fraction of photons that are still there at the end. It is reported separately from fidelity, since a perfect state that rarely arrives is not much use.
- **Threshold**: the level a number must beat before something is worthwhile. For a memory, the threshold is the efficiency below which a simple measure-and-resend method does as well.
- **Classical benchmark, or bound**: the best score a non-quantum method can reach on the same task. A quantum device earns credit only for beating it.
- **Chain**: all the stages a photon passes through, from source to detector. The overall efficiency is the product of the stages.
- **Reliability (of a herald)**: of the runs where the herald fires, the fraction in which the output is actually valid.

## 7. Words and symbols for reading the math

You will see a few symbols. None of them needs more than this explanation. [Appendix 4](A4-math-refresher.md) has a longer, gentle refresher.

- **Ket**: a way of writing a state, with a vertical bar on the left and an angle bracket on the right. The ket for address 01 is written with 01 between them. It just means "the state called 01".
- **√2 (square root of 2)**: a blend of two equal parts has each part multiplied by 1 over √2 (about 0.707), so that the probabilities, which are the squares, add to 1.
- **⊗ (tensor product)**: "combine these two parts into one joint system". It is how a polarization state and a twist state form one photon's state.
- **i**: the imaginary unit, a number whose square is −1. It appears because phase shifts are written as complex numbers.
- **Matrix**: a grid of numbers that describes an operation on a state. A 4 × 4 matrix acts on a four-level state.
- **Unitary**: see section 3. The matrices for ideal operations are unitary.
- **%**: a percentage. 56.9 % means 0.569.
- **n̄, F, η**: n̄ is the average noise photon number, F is fidelity, and η (eta) is a fraction of light that passes, an efficiency.

## 8. The honesty labels

Every number and claim in the library has one of these labels. They are explained in [Start Here](00-start-here.md).

- **DERIVED**: worked out by mathematics from stated assumptions.
- **REPORTED**: a published source says so, and we say how much of it we read.
- **SIMULATED**: the output of a model.
- **ASSUMED**: a number we chose.
- **PROPOSED**: an idea, not shown to work.
- **MEASURED**: measured by PhaseKeep in a lab. **None yet.**
- **UNVERIFIED**: supplied or remembered but not checked.
- **BLOCKED**: cannot move forward without something we lack.

>
> **In plain words**
> **If you remember only one thing:** a nice-looking number is worth only as much as the label next to it. Please check the label.


## Where to go next

Start with [Start Here](00-start-here.md) if you have not read it, then [Volume 1](01-light.md). If a word in a later volume does not make sense, look here first, then in [Appendix 1](A1-glossary.md) and the [FAQ](A5-faq.md).


---
*(c) 2026 Tyler O'Bryan, where applicable. PhaseKeep Research. Text CC BY 4.0, code MIT. AI-assisted research, documentation and numerical analysis. Draft for technical review.*

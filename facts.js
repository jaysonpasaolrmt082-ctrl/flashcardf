// Science fact bank + question maker. Every fact can be asked many different ways
// (identify, what-does-it-do, true/false, odd one out, two statements, analogy,
// matching pairs, "who am I?" riddle), picked at random each time it is played.
//
// Group fields: g/gp = kind of thing (singular/plural), art = use "the" before the term,
//               topic = which deck it belongs to.
// Fact fields:  t = term, d = what it does/is (verb phrase that fits after the term),
//               s = short cue for analogies and matching, x = extra riddle clue,
//               k = other accepted answers, pl = plural term (uses plural verbs).
(function () {
  var TOPICS = [
    { id: "tBody", name: "Cells & the human body" },
    { id: "tLife", name: "Plants, animals & ecology" },
    { id: "tMatter", name: "Matter & chemistry" },
    { id: "tEnergy", name: "Energy, forces & waves" },
    { id: "tEarth", name: "Earth, weather & hazards" },
    { id: "tSpace", name: "Space" },
    { id: "tPeople", name: "Scientists, agencies & word parts" }
  ];

  function F(t, d, o) { o = o || {}; o.t = t; o.d = d; return o; }

  var GROUPS = [
    { topic: "tBody", g: "cell part", gp: "cell parts", art: true, f: [
      F("Nucleus", "controls the cell's activities and holds its DNA", { s: "control center", x: "I am usually round and sit near the middle of the cell." }),
      F("Mitochondrion", "releases energy from food", { s: "energy", k: ["mitochondria"], x: "People call me the powerhouse of the cell." }),
      F("Chloroplast", "makes food using sunlight in plant cells", { s: "photosynthesis", x: "I am green because of chlorophyll." }),
      F("Cell membrane", "controls what enters and leaves the cell", { s: "gatekeeper", x: "Every cell, plant or animal, has me as its thin outer layer." }),
      F("Cell wall", "gives plant cells a stiff, boxy shape", { s: "support", x: "Animal cells do not have me." }),
      F("Ribosome", "makes proteins", { s: "proteins", x: "I am one of the tiniest parts of the cell." }),
      F("Vacuole", "stores water, food, and wastes", { s: "storage", x: "In plant cells I am one big sac." })
    ]},
    { topic: "tBody", g: "organ", gp: "organs", art: true, f: [
      F("Heart", "pumps blood around the body", { s: "pumping blood", x: "I have four chambers." }),
      F("Lungs", "take in oxygen and give off carbon dioxide", { pl: true, s: "breathing", k: ["lung"], x: "We have millions of tiny air sacs called alveoli." }),
      F("Kidneys", "filter the blood and make urine", { pl: true, s: "filtering blood", k: ["kidney"], x: "We are bean-shaped and found near your lower back." }),
      F("Liver", "makes bile and removes poisons from the blood", { s: "bile", x: "I am the largest organ inside the body." }),
      F("Stomach", "mixes food with acid to start digesting proteins", { s: "churning food", x: "I am a J-shaped bag of muscle." }),
      F("Small intestine", "absorbs most of the nutrients from food", { s: "absorbing nutrients", x: "I am about 6 meters long and folded inside you." }),
      F("Large intestine", "absorbs water from undigested food", { s: "absorbing water", k: ["colon"], x: "I come right after the small intestine." }),
      F("Pancreas", "makes insulin and digestive juices", { s: "insulin", x: "When I don't make enough insulin, a person can get diabetes." }),
      F("Skin", "covers and protects the whole body", { s: "protection", x: "I am the largest organ of all." })
    ]},
    { topic: "tBody", g: "part of the blood", gp: "parts of the blood", art: true, f: [
      F("Red blood cells", "carry oxygen using hemoglobin", { pl: true, s: "oxygen", k: ["rbc", "red blood cell"], x: "We have no nucleus and give blood its color." }),
      F("White blood cells", "fight germs and infection", { pl: true, s: "fighting germs", k: ["wbc", "white blood cell"], x: "We are the body's soldiers." }),
      F("Platelets", "help the blood clot when you get a cut", { pl: true, s: "clotting", k: ["platelet"], x: "We are tiny cell pieces." }),
      F("Plasma", "is the yellowish liquid that carries blood cells and nutrients", { s: "liquid", x: "I make up more than half of your blood." })
    ]},
    { topic: "tBody", g: "blood vessel", gp: "blood vessels", art: true, f: [
      F("Arteries", "carry blood away from the heart", { pl: true, s: "away from the heart", k: ["artery"], x: "Our walls are thick and strong." }),
      F("Veins", "carry blood back to the heart", { pl: true, s: "back to the heart", k: ["vein"], x: "We have valves so blood does not flow backward." }),
      F("Capillaries", "let oxygen and food pass into the body's cells", { pl: true, s: "exchange", k: ["capillary"], x: "We are the tiniest blood vessels, thinner than a hair." })
    ]},
    { topic: "tBody", g: "part of the brain", gp: "parts of the brain", art: true, f: [
      F("Cerebrum", "controls thinking, memory, and the senses", { s: "thinking", x: "I am the largest part of the brain." }),
      F("Cerebellum", "controls balance and coordination", { s: "balance", x: "I sit at the back, below the biggest part of the brain." }),
      F("Brainstem", "controls breathing and heartbeat", { s: "breathing and heartbeat", k: ["brain stem", "medulla", "medulla oblongata"], x: "I connect the brain to the spinal cord." })
    ]},
    { topic: "tBody", g: "body system", gp: "body systems", art: true, f: [
      F("Circulatory system", "moves blood, oxygen, and nutrients around the body", { s: "heart and blood vessels", k: ["circulatory"] }),
      F("Respiratory system", "brings in oxygen and removes carbon dioxide", { s: "lungs", k: ["respiratory"] }),
      F("Digestive system", "breaks food down into nutrients", { s: "stomach and intestines", k: ["digestive"] }),
      F("Nervous system", "sends messages through the brain and nerves", { s: "brain and nerves", k: ["nervous"] }),
      F("Skeletal system", "supports the body and protects the organs", { s: "bones", k: ["skeletal"] }),
      F("Muscular system", "moves the body by pulling on bones", { s: "muscles", k: ["muscular"] }),
      F("Excretory system", "removes liquid wastes from the body", { s: "kidneys and bladder", k: ["excretory", "urinary system"] }),
      F("Endocrine system", "makes hormones that control growth and mood", { s: "glands and hormones", k: ["endocrine"] }),
      F("Immune system", "defends the body against germs", { s: "white blood cells", k: ["immune"] })
    ]},
    { topic: "tBody", g: "bone", gp: "bones", art: true, f: [
      F("Femur", "is the longest bone, found in the thigh", { s: "thigh", k: ["thigh bone"] }),
      F("Skull", "protects the brain", { s: "head", k: ["cranium"] }),
      F("Ribs", "protect the heart and lungs", { pl: true, s: "chest", k: ["rib cage", "rib"] }),
      F("Stapes", "is the smallest bone, found in the ear", { s: "ear", k: ["stirrup"] }),
      F("Vertebrae", "make up the backbone and protect the spinal cord", { pl: true, s: "backbone", k: ["vertebra", "spine", "backbone"] }),
      F("Patella", "is the kneecap", { s: "knee", k: ["kneecap"] })
    ]},

    { topic: "tLife", g: "plant part", gp: "plant parts", art: true, f: [
      F("Roots", "absorb water and hold the plant in the soil", { pl: true, s: "absorbing water", k: ["root"] }),
      F("Stem", "holds the plant up and carries water and food", { s: "support", k: ["stalk"] }),
      F("Leaves", "make food by photosynthesis", { pl: true, s: "making food", k: ["leaf"] }),
      F("Xylem", "carries water up from the roots", { s: "water up", x: "My name starts with a letter that also starts xylophone." }),
      F("Phloem", "carries food from the leaves to the rest of the plant", { s: "food down" }),
      F("Stomata", "let air and water vapor in and out of the leaves", { pl: true, s: "tiny pores", k: ["stoma", "stomates"] })
    ]},
    { topic: "tLife", g: "flower part", gp: "flower parts", art: true, f: [
      F("Stamen", "is the male part that makes pollen", { s: "pollen", k: ["anther"] }),
      F("Pistil", "is the female part of the flower", { s: "female part", k: ["carpel"] }),
      F("Petals", "attract insects with bright colors", { pl: true, s: "color", k: ["petal"] }),
      F("Sepals", "protect the flower while it is still a bud", { pl: true, s: "bud protection", k: ["sepal"] }),
      F("Ovary", "grows into the fruit after fertilization", { s: "fruit" }),
      F("Stigma", "is the sticky tip that catches pollen", { s: "sticky tip" })
    ]},
    { topic: "tLife", g: "plant process", gp: "plant processes", art: false, f: [
      F("Photosynthesis", "turns sunlight, water, and carbon dioxide into food and oxygen", { s: "making food" }),
      F("Transpiration", "is the loss of water vapor through the leaves", { s: "losing water" }),
      F("Pollination", "is the transfer of pollen to the stigma", { s: "moving pollen" }),
      F("Germination", "is when a seed starts to sprout", { s: "sprouting" }),
      F("Respiration", "releases energy from food using oxygen", { s: "releasing energy", k: ["cellular respiration"] })
    ]},
    { topic: "tLife", g: "relationship between living things", gp: "relationships", art: false, f: [
      F("Mutualism", "happens when both living things benefit, like bees and flowers", { s: "both benefit" }),
      F("Commensalism", "happens when one benefits and the other is not affected, like an orchid on a tree", { s: "one benefits, one unaffected" }),
      F("Parasitism", "happens when one benefits and the other is harmed, like lice on a dog", { s: "one is harmed" }),
      F("Predation", "happens when one animal hunts and eats another", { s: "hunting" }),
      F("Competition", "happens when living things need the same food or space", { s: "same resources" })
    ]},
    { topic: "tLife", g: "role in a food chain", gp: "roles in a food chain", art: false, f: [
      F("Producers", "make their own food, like plants", { pl: true, s: "plants", k: ["producer"] }),
      F("Herbivores", "eat only plants", { pl: true, s: "plants only", k: ["herbivore", "primary consumer", "primary consumers"] }),
      F("Carnivores", "eat only other animals", { pl: true, s: "meat only", k: ["carnivore"] }),
      F("Omnivores", "eat both plants and animals", { pl: true, s: "plants and meat", k: ["omnivore"] }),
      F("Decomposers", "break down dead plants and animals", { pl: true, s: "breaking down", k: ["decomposer"] })
    ]},
    { topic: "tLife", g: "vertebrate group", gp: "vertebrate groups", art: false, f: [
      F("Mammals", "have hair or fur and feed their young with milk", { pl: true, s: "milk", k: ["mammal"] }),
      F("Birds", "have feathers and lay hard-shelled eggs", { pl: true, s: "feathers", k: ["bird"] }),
      F("Reptiles", "have dry, scaly skin and are cold-blooded", { pl: true, s: "scales", k: ["reptile"] }),
      F("Amphibians", "live in water when young and on land as adults", { pl: true, s: "moist skin", k: ["amphibian"] }),
      F("Fish", "breathe with gills and swim with fins", { pl: true, s: "gills" })
    ]},
    { topic: "tLife", g: "invertebrate group", gp: "invertebrate groups", art: false, f: [
      F("Insects", "have 6 legs and 3 body parts", { pl: true, s: "6 legs", k: ["insect"] }),
      F("Arachnids", "have 8 legs, like spiders and scorpions", { pl: true, s: "8 legs", k: ["arachnid"] }),
      F("Mollusks", "have soft bodies, often inside a shell, like snails and squid", { pl: true, s: "soft body", k: ["mollusk", "molluscs", "mollusc"] }),
      F("Crustaceans", "have hard shells and many legs, like crabs and shrimp", { pl: true, s: "crabs and shrimp", k: ["crustacean"] }),
      F("Annelids", "are segmented worms, like earthworms", { pl: true, s: "segmented worms", k: ["annelid", "segmented worms"] })
    ]},
    { topic: "tLife", g: "disease", gp: "diseases", art: false, f: [
      F("Dengue", "is spread by the daytime-biting Aedes mosquito", { s: "Aedes mosquito" }),
      F("Malaria", "is spread by the Anopheles mosquito", { s: "Anopheles mosquito" }),
      F("Tuberculosis", "is a bacterial disease that mainly attacks the lungs", { s: "lungs", k: ["tb"] }),
      F("Leptospirosis", "spreads through floodwater mixed with rat urine", { s: "floodwater" }),
      F("Rabies", "spreads through the bite of an infected dog or cat", { s: "dog bite" }),
      F("Cholera", "spreads through dirty drinking water and causes severe diarrhea", { s: "dirty water" })
    ]},

    { topic: "tMatter", g: "change of state", gp: "changes of state", art: false, f: [
      F("Melting", "changes a solid into a liquid", { s: "solid to liquid" }),
      F("Freezing", "changes a liquid into a solid", { s: "liquid to solid" }),
      F("Evaporation", "changes a liquid into a gas", { s: "liquid to gas", k: ["boiling", "vaporization"] }),
      F("Condensation", "changes a gas into a liquid", { s: "gas to liquid" }),
      F("Sublimation", "changes a solid straight into a gas", { s: "solid to gas" }),
      F("Deposition", "changes a gas straight into a solid", { s: "gas to solid" })
    ]},
    { topic: "tMatter", g: "way to separate mixtures", gp: "ways to separate mixtures", art: false, f: [
      F("Filtration", "separates solid bits from a liquid using filter paper", { s: "filter paper", k: ["filtering"] }),
      F("Decantation", "pours off the liquid after the solids settle", { s: "pouring off", k: ["decanting"] }),
      F("Distillation", "separates liquids by boiling and cooling the vapor", { s: "boiling points" }),
      F("Magnetic separation", "pulls iron bits out of a mixture", { s: "magnet", k: ["magnet", "using a magnet"] }),
      F("Sieving", "separates particles by size using a mesh", { s: "mesh", k: ["sifting"] }),
      F("Chromatography", "separates the colors in ink", { s: "ink colors", k: ["paper chromatography"] })
    ]},
    { topic: "tMatter", g: "type of mixture", gp: "types of mixtures", art: "a", f: [
      F("Solution", "looks the same throughout, like salt water", { s: "salt water", k: ["homogeneous mixture"] }),
      F("Suspension", "has particles that settle when left alone, like muddy water", { s: "muddy water" }),
      F("Colloid", "has tiny particles that stay mixed but scatter light, like milk", { s: "milk" })
    ]},
    { topic: "tMatter", g: "chemical element", gp: "chemical elements", art: false, f: [
      F("Sodium", "has the chemical symbol Na", { s: "Na" }),
      F("Potassium", "has the chemical symbol K", { s: "K" }),
      F("Iron", "has the chemical symbol Fe", { s: "Fe" }),
      F("Gold", "has the chemical symbol Au", { s: "Au" }),
      F("Silver", "has the chemical symbol Ag", { s: "Ag" }),
      F("Copper", "has the chemical symbol Cu", { s: "Cu" }),
      F("Lead", "has the chemical symbol Pb", { s: "Pb" }),
      F("Mercury", "has the chemical symbol Hg", { s: "Hg", x: "I am the only metal that is liquid at room temperature." })
    ]},
    { topic: "tMatter", g: "kind of substance", gp: "kinds of substances", art: false, f: [
      F("Acids", "taste sour and have a pH below 7", { pl: true, s: "sour", k: ["acid"] }),
      F("Bases", "taste bitter, feel slippery, and have a pH above 7", { pl: true, s: "slippery", k: ["base", "alkali"] }),
      F("Neutral substances", "have a pH of exactly 7, like pure water", { pl: true, s: "pH 7", k: ["neutral"] })
    ]},

    { topic: "tEnergy", g: "form of energy", gp: "forms of energy", art: false, f: [
      F("Kinetic energy", "is the energy of a moving object", { s: "motion", k: ["kinetic"] }),
      F("Potential energy", "is energy stored because of position, like a coconut up a tree", { s: "position", k: ["potential"] }),
      F("Thermal energy", "is heat energy from moving particles", { s: "heat", k: ["heat energy", "thermal"] }),
      F("Chemical energy", "is stored in food, fuel, and batteries", { s: "food and batteries", k: ["chemical"] }),
      F("Electrical energy", "is carried by moving electric charges", { s: "electric charges", k: ["electricity", "electrical"] }),
      F("Sound energy", "is carried by vibrations", { s: "vibrations", k: ["sound"] })
    ]},
    { topic: "tEnergy", g: "energy source", gp: "energy sources", art: false, f: [
      F("Geothermal energy", "uses heat from inside the Earth, as in Tiwi, Albay", { s: "heat inside Earth", k: ["geothermal"] }),
      F("Hydroelectric energy", "uses flowing water, like the Agus River plants in Mindanao", { s: "flowing water", k: ["hydroelectric", "hydropower", "hydro"] }),
      F("Solar energy", "uses sunlight", { s: "sunlight", k: ["solar"] }),
      F("Wind energy", "uses moving air, like the Bangui windmills in Ilocos Norte", { s: "moving air", k: ["wind"] }),
      F("Biomass energy", "burns plant and animal waste for fuel", { s: "plant waste", k: ["biomass"] }),
      F("Coal", "is a fossil fuel that pollutes the air and will run out", { s: "fossil fuel" })
    ]},
    { topic: "tEnergy", g: "way heat travels", gp: "ways heat travels", art: false, f: [
      F("Conduction", "moves heat through direct contact, like a hot spoon handle", { s: "touching" }),
      F("Convection", "moves heat by flowing liquids or gases, like boiling water", { s: "flowing" }),
      F("Radiation", "moves heat as waves, even through empty space, like sunlight", { s: "waves through space" })
    ]},
    { topic: "tEnergy", g: "wave behavior", gp: "wave behaviors", art: false, f: [
      F("Reflection", "is the bouncing back of a wave, like an echo", { s: "bouncing back" }),
      F("Refraction", "is the bending of a wave as it enters a new material, like a bent-looking straw in water", { s: "bending" }),
      F("Diffraction", "is the spreading of waves around corners and through openings", { s: "spreading around corners" }),
      F("Absorption", "is when a material takes in a wave's energy, like dark clothes in sunlight", { s: "taking in" }),
      F("Dispersion", "is the splitting of white light into colors, like a rainbow", { s: "rainbow" })
    ]},
    { topic: "tEnergy", g: "part of a wave", gp: "parts of a wave", art: "the", f: [
      F("Crest", "is the highest point of a wave", { s: "top" }),
      F("Trough", "is the lowest point of a wave", { s: "bottom" }),
      F("Amplitude", "is the height of a wave from its rest position", { s: "height" }),
      F("Wavelength", "is the distance from one crest to the next", { s: "crest to crest" }),
      F("Frequency", "is the number of waves that pass each second", { s: "waves per second" })
    ]},
    { topic: "tEnergy", g: "simple machine", gp: "simple machines", art: "a", f: [
      F("Lever", "is a bar that turns on a fulcrum, like a seesaw", { s: "seesaw" }),
      F("Pulley", "is a wheel with a rope used to lift loads, like on a flagpole", { s: "flagpole" }),
      F("Inclined plane", "is a ramp that makes lifting easier", { s: "ramp", k: ["ramp"] }),
      F("Wedge", "splits things apart, like an axe or knife", { s: "axe" }),
      F("Screw", "is an inclined plane wrapped around a rod, like a jar lid", { s: "jar lid" }),
      F("Wheel and axle", "is a large wheel turning a small rod, like a doorknob", { s: "doorknob" })
    ]},
    { topic: "tEnergy", g: "force", gp: "forces", art: false, f: [
      F("Gravity", "pulls objects toward the Earth", { s: "falling" }),
      F("Friction", "slows down motion between two surfaces that rub", { s: "rubbing" }),
      F("Magnetism", "pulls on iron, nickel, and cobalt", { s: "iron nails" }),
      F("Buoyancy", "pushes objects up in water so they float", { s: "floating", k: ["buoyant force", "upthrust"] }),
      F("Air resistance", "slows objects falling or moving through air", { s: "parachute", k: ["drag"] })
    ]},
    { topic: "tEnergy", g: "unit", gp: "units", art: "the", f: [
      F("Newton", "is the unit of force", { s: "force", k: ["newtons", "n"] }),
      F("Joule", "is the unit of energy", { s: "energy", k: ["joules", "j"] }),
      F("Watt", "is the unit of power", { s: "power", k: ["watts", "w"] }),
      F("Volt", "is the unit of voltage", { s: "voltage", k: ["volts", "v"] }),
      F("Ampere", "is the unit of electric current", { s: "current", k: ["amperes", "amp", "amps", "a"] }),
      F("Ohm", "is the unit of electrical resistance", { s: "resistance", k: ["ohms"] }),
      F("Hertz", "is the unit of frequency", { s: "frequency", k: ["hz"] }),
      F("Decibel", "is the unit of sound loudness", { s: "loudness", k: ["decibels", "db"] })
    ]},
    { topic: "tEnergy", g: "electricity word", gp: "electricity words", art: "a", f: [
      F("Conductor", "lets electricity flow easily, like copper", { s: "copper" }),
      F("Insulator", "blocks the flow of electricity, like rubber", { s: "rubber" }),
      F("Series circuit", "has only one path, so all bulbs go out if one breaks", { s: "one path", k: ["series"] }),
      F("Parallel circuit", "has many paths, so other bulbs stay lit if one breaks", { s: "many paths", k: ["parallel"] }),
      F("Switch", "opens and closes a circuit", { s: "on and off" })
    ]},

    { topic: "tEarth", g: "science instrument", gp: "science instruments", art: "a", f: [
      F("Thermometer", "measures temperature", { s: "temperature" }),
      F("Barometer", "measures air pressure", { s: "air pressure" }),
      F("Anemometer", "measures wind speed", { s: "wind speed" }),
      F("Wind vane", "shows wind direction", { s: "wind direction", k: ["weather vane"] }),
      F("Hygrometer", "measures humidity, the water vapor in the air", { s: "humidity" }),
      F("Rain gauge", "measures how much rain fell", { s: "rainfall" }),
      F("Seismograph", "records earthquakes", { s: "earthquakes", k: ["seismometer"] }),
      F("Microscope", "makes tiny things look bigger", { s: "tiny things" }),
      F("Telescope", "makes faraway objects look closer", { s: "faraway objects" })
    ]},
    { topic: "tEarth", g: "layer of the Earth", gp: "layers of the Earth", art: "the", f: [
      F("Crust", "is the thin, rocky outer layer we live on", { s: "outermost" }),
      F("Mantle", "is the thickest layer, made of hot, slowly flowing rock", { s: "thickest" }),
      F("Outer core", "is a layer of liquid iron and nickel", { s: "liquid metal" }),
      F("Inner core", "is the solid, hottest center of the Earth", { s: "hottest" })
    ]},
    { topic: "tEarth", g: "layer of the atmosphere", gp: "layers of the atmosphere", art: "the", f: [
      F("Troposphere", "is the lowest layer, where all weather happens", { s: "weather" }),
      F("Stratosphere", "contains the ozone layer", { s: "ozone" }),
      F("Mesosphere", "is where most meteors burn up", { s: "meteors" }),
      F("Thermosphere", "is where auroras happen and the space station orbits", { s: "auroras" }),
      F("Exosphere", "is the outermost layer that fades into space", { s: "edge of space" })
    ]},
    { topic: "tEarth", g: "type of rock", gp: "types of rocks", art: false, f: [
      F("Igneous rock", "forms when magma or lava cools, like granite and pumice", { s: "cooled lava", k: ["igneous"] }),
      F("Sedimentary rock", "forms from layers of sand and mud pressed together, like sandstone", { s: "layers", k: ["sedimentary"] }),
      F("Metamorphic rock", "forms when heat and pressure change a rock, like marble", { s: "heat and pressure", k: ["metamorphic"] })
    ]},
    { topic: "tEarth", g: "earthquake word", gp: "earthquake words", art: "the", f: [
      F("Epicenter", "is the spot on the surface right above where a quake starts", { s: "surface spot", k: ["epicentre"] }),
      F("Focus", "is the point inside the Earth where a quake starts", { s: "starting point", k: ["hypocenter"] }),
      F("Fault", "is a crack in the Earth's crust where rocks move", { art: "a", s: "crack", k: ["fault line"] }),
      F("Magnitude", "measures the energy released at the quake's source", { art: "", s: "energy" }),
      F("Intensity", "measures how strongly the shaking is felt in a place", { art: "", s: "shaking felt" }),
      F("Aftershock", "is a smaller quake that follows the main one", { art: "a", s: "after the main quake" })
    ]},
    { topic: "tEarth", g: "natural hazard", gp: "natural hazards", art: "a", f: [
      F("Storm surge", "is seawater pushed onto land by a strong typhoon", { s: "typhoon" }),
      F("Tsunami", "is a series of giant waves caused by an undersea earthquake", { s: "undersea quake" }),
      F("Landslide", "is soil and rocks sliding down a slope", { s: "slope", k: ["mudslide"] }),
      F("Flash flood", "is sudden flooding after very heavy rain", { s: "sudden" }),
      F("Liquefaction", "is wet ground acting like a liquid during an earthquake", { art: "", s: "soil like liquid" })
    ]},
    { topic: "tEarth", g: "Philippine weather word", gp: "Philippine weather words", art: "the", f: [
      F("Amihan", "is the cool northeast monsoon, from about November to February", { s: "cool wind", k: ["northeast monsoon"] }),
      F("Habagat", "is the wet southwest monsoon that brings heavy rain", { s: "rainy wind", k: ["southwest monsoon"] }),
      F("El Niño", "brings drought and less rain to the Philippines", { art: "", s: "drought", k: ["el nino"] }),
      F("La Niña", "brings more rain than normal to the Philippines", { art: "", s: "extra rain", k: ["la nina"] })
    ]},

    { topic: "tSpace", g: "space object", gp: "space objects", art: "a", f: [
      F("Star", "makes its own light and heat, like the Sun", { s: "own light" }),
      F("Planet", "orbits a star and does not make its own light", { s: "orbits a star" }),
      F("Comet", "is a ball of ice and dust with a glowing tail", { s: "tail" }),
      F("Asteroid", "is a rocky object, mostly found between Mars and Jupiter", { s: "rocky belt" }),
      F("Meteor", "is the streak of light when a space rock burns in the air", { s: "shooting star", k: ["shooting star"] }),
      F("Meteorite", "is a space rock that reaches the ground", { s: "lands on Earth" })
    ]},
    { topic: "tSpace", g: "planet", gp: "planets", proper: true, art: false, f: [
      F("Mercury", "is the closest planet to the Sun and the smallest", { s: "closest" }),
      F("Venus", "is the hottest planet because its thick air traps heat", { s: "hottest" }),
      F("Earth", "is the only planet known to have life", { s: "life" }),
      F("Mars", "is called the Red Planet", { s: "red" }),
      F("Jupiter", "is the largest planet, with the Great Red Spot", { s: "largest" }),
      F("Saturn", "has the most famous rings", { s: "rings" }),
      F("Uranus", "spins on its side", { s: "tilted" }),
      F("Neptune", "is the farthest planet from the Sun", { s: "farthest" })
    ]},
    { topic: "tSpace", g: "Moon and eclipse word", gp: "Moon and eclipse words", art: "a", f: [
      F("New moon", "is when the Moon's dark side faces Earth", { s: "dark" }),
      F("Full moon", "is when the Moon's whole lit side faces Earth", { s: "all lit" }),
      F("Solar eclipse", "is when the Moon blocks the Sun", { s: "Sun blocked" }),
      F("Lunar eclipse", "is when Earth's shadow falls on the Moon", { s: "Moon darkened" }),
      F("Waxing crescent", "is a thin, growing sliver of the Moon after new moon", { s: "growing sliver" })
    ]},

    { topic: "tPeople", g: "word part", gp: "word parts", proper: true, art: false, f: [
      F("Hydro", "means water", { s: "water" }),
      F("Photo", "means light", { s: "light" }),
      F("Geo", "means Earth", { s: "Earth" }),
      F("Bio", "means life", { s: "life" }),
      F("Thermo", "means heat", { s: "heat" }),
      F("Peri", "means near or around", { s: "near" }),
      F("Ecto", "means outside", { s: "outside" }),
      F("-itis", "means swelling or inflammation", { s: "swelling", k: ["itis"] })
    ]},
    { topic: "tPeople", g: "scientist", gp: "scientists", proper: true, art: false, f: [
      F("Isaac Newton", "gave us the three laws of motion and the law of gravity", { s: "laws of motion", k: ["newton"] }),
      F("Charles Darwin", "explained evolution by natural selection", { s: "evolution", k: ["darwin"] }),
      F("Gregor Mendel", "is the father of genetics, who studied pea plants", { s: "pea plants", k: ["mendel"] }),
      F("Marie Curie", "studied radioactivity and won two Nobel Prizes", { s: "radioactivity", k: ["curie"] }),
      F("Louis Pasteur", "invented pasteurization and a rabies vaccine", { s: "pasteurization", k: ["pasteur"] }),
      F("Alexander Fleming", "discovered penicillin, the first antibiotic", { s: "penicillin", k: ["fleming"] }),
      F("Galileo Galilei", "used a telescope to discover Jupiter's moons", { s: "telescope", k: ["galileo"] })
    ]},
    { topic: "tPeople", g: "Filipino scientist", gp: "Filipino scientists", proper: true, art: false, f: [
      F("Fe del Mundo", "was a pediatrician who improved the baby incubator", { s: "baby incubator", k: ["dr fe del mundo", "del mundo"] }),
      F("Angel Alcala", "set up marine sanctuaries like Apo Island", { s: "marine sanctuaries", k: ["alcala"] }),
      F("Gregorio Zara", "invented a two-way television telephone (videophone)", { s: "videophone", k: ["zara"] }),
      F("Ramon Barba", "found a way to make mango trees flower even out of season", { s: "mango flowering", k: ["barba"] }),
      F("Maria Orosa", "was a food scientist who created banana ketchup", { s: "banana ketchup", k: ["orosa"] }),
      F("Diosdado Banatao", "designed computer chips used around the world", { s: "computer chips", k: ["banatao"] })
    ]},
    { topic: "tPeople", g: "Philippine agency", gp: "Philippine agencies", proper: true, art: false, f: [
      F("PAGASA", "gives weather forecasts and typhoon wind signals", { s: "weather" }),
      F("PHIVOLCS", "watches volcanoes, earthquakes, and tsunamis", { s: "volcanoes and earthquakes" }),
      F("DOST", "leads science and technology in the country", { s: "science and technology" }),
      F("PhilSA", "runs the country's space program", { s: "space", k: ["philippine space agency"] }),
      F("DENR", "protects the environment and natural resources", { s: "environment" }),
      F("DOH", "takes care of public health", { s: "health" })
    ]}
  ];

  // ---------- helpers ----------
  function R(a, b) { return a + Math.floor(Math.random() * (b - a + 1)); }
  function P(a) { return a[R(0, a.length - 1)]; }
  function shuffle(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  function cap(s) { return s.charAt(0).toUpperCase() + s.slice(1); }
  function an(w) { return /^[aeio]|^u(?!ni)/i.test(w) ? "an " + w : "a " + w; }
  // "pumps blood" -> "pump blood" so riddles can say "I pump blood".
  function firstPerson(d) {
    var m = d.match(/^(\S+)(.*)$/), v = m[1], rest = m[2];
    var map = { is: "am", has: "have", does: "do" };
    if (map[v]) v = map[v];
    else if (/ies$/.test(v)) v = v.replace(/ies$/, "y");
    else if (/(ches|shes|sses|xes)$/.test(v)) v = v.replace(/es$/, "");
    else if (/[^s]s$/.test(v)) v = v.replace(/s$/, "");
    return v + rest;
  }

  var ALLF = [];
  GROUPS.forEach(function (g, gi) { g.f.forEach(function (f, fi) { f.gi = gi; f.fid = gi + "." + fi; ALLF.push(f); }); });
  function grp(f) { return GROUPS[f.gi]; }
  function sibs(f, samePl) { return grp(f).f.filter(function (x) { return x !== f && (!samePl || !!x.pl === !!f.pl); }); }
  function outsiders(f) { return ALLF.filter(function (x) { return x.gi !== f.gi && x.t !== f.t; }); }
  // How the term reads at the start of a sentence: "The heart", "Photosynthesis", "PAGASA".
  function subj(f) {
    var t = f.t, art = f.art !== undefined ? f.art : grp(f).art;
    if (art === true) art = "the";
    if (!art) return t;
    var low = /^[A-Z]{2,}/.test(t) ? t : t.charAt(0).toLowerCase() + t.slice(1);
    return art === "a" ? cap(an(low)) : "The " + low;
  }
  function lowSubj(f) {
    var x = subj(f);
    if (x === f.t) return grp(f).proper || /^[A-Z]{2,}/.test(x) ? x : x.charAt(0).toLowerCase() + x.slice(1);
    return x.replace(/^(The|An|A) /, function (m) { return m.toLowerCase(); });
  }
  function kindOf(f) { return f.pl ? grp(f).gp : grp(f).g; }
  function sentence(f, d) { return subj(f) + " " + (d || f.d) + "."; }
  function base(f, extra) {
    return Object.assign({ cat: cap(grp(f).g), a: f.t, k: f.k, e: sentence(f) + (f.x ? " " + f.x : ""), h: [f.t], fact: f.fid }, extra);
  }
  function mcFrom(right, wrongs, extra) {
    var all = shuffle([right].concat(wrongs.slice(0, 3)));
    var i = all.indexOf(right);
    return Object.assign(extra, { c: all, a: "ABCD"[i] + " · " + right });
  }

  // ---------- question shapes ----------
  var SHAPES = {
    identify: function (f) { // typed
      var k = kindOf(f), d = f.d;
      var q = P([
        "Identify the " + k + ": it " + d + ".",
        "What " + k + " " + d + "?",
        "Name the " + k + " that " + d + ".",
        "Fill in the blank: The ________ " + d + "."
      ]);
      if (q.indexOf("Fill in") === 0 && !grp(f).art) q = "Fill in the blank: ________ " + d + ".";
      return base(f, { q: q, h: [d] });
    },
    pickTerm: function (f) { // which term fits the description
      var w = shuffle(sibs(f)).map(function (x) { return x.t; });
      if (w.length < 3) w = w.concat(shuffle(outsiders(f)).slice(0, 3 - w.length).map(function (x) { return x.t; }));
      return mcFrom(f.t, w, base(f, { q: "Which " + kindOf(f) + " " + f.d + "?", h: [f.d] }));
    },
    pickDesc: function (f) { // which description fits the term
      var w = shuffle(sibs(f, true)).concat(shuffle(sibs(f, false))).map(function (x) { return cap(x.d); });
      w = w.filter(function (x, i) { return w.indexOf(x) === i; });
      if (w.length < 3) return null;
      return mcFrom(cap(f.d), w, base(f, { q: P(["Which statement correctly describes " + lowSubj(f) + "?", "What is true about " + lowSubj(f) + "?"]), a: cap(f.d), h: [f.t] }));
    },
    trueFalse: function (f) {
      var s = sibs(f, true);
      var lie = s.length && Math.random() < 0.55 ? P(s) : null;
      var claim = sentence(f, lie ? lie.d : f.d);
      return base(f, { q: "TRUE or FALSE: " + claim, c: ["True", "False"], a: lie ? "B · False" : "A · True",
        e: lie ? "False. " + sentence(f) + " " + sentence(lie) : "True. " + sentence(f), h: [f.t] });
    },
    oddOne: function (f) { // f is the outsider
      var groups = GROUPS.filter(function (g, gi) { return gi !== f.gi && g.f.length >= 3 && g.topic === grp(f).topic; });
      if (!groups.length) groups = GROUPS.filter(function (g, gi) { return gi !== f.gi && g.f.length >= 3; });
      var g = P(groups), three = shuffle(g.f).slice(0, 3).map(function (x) { return x.t; });
      if (g.f.some(function (x) { return x.t.toLowerCase() === f.t.toLowerCase(); })) return null; // e.g. Mercury is a planet AND an element
      return mcFrom(f.t, three, base(f, { q: P(["Odd one out: which one does NOT belong with the others?", "Which of these is NOT one of the " + g.gp + "?"]),
        e: three.join(", ") + " are all " + g.gp + ". " + sentence(f), h: ["NOT"] }));
    },
    twoStatements: function (f) {
      var s = sibs(f, true), g = P(sibs(f)) || P(outsiders(f));
      if (!s.length || !g) return null;
      var t1 = Math.random() < 0.5, t2 = Math.random() < 0.5;
      var gs = sibs(g, true).filter(function (x) { return x !== f; });
      if (!gs.length) t2 = true;
      var lie1 = P(s), lie2 = gs.length ? P(gs) : null;
      var st1 = sentence(f, t1 ? f.d : lie1.d), st2 = sentence(g, t2 ? g.d : lie2.d);
      var opts = ["Both statements are true", "Only statement I is true", "Only statement II is true", "Both statements are false"];
      var right = t1 && t2 ? 0 : t1 ? 1 : t2 ? 2 : 3;
      return { cat: cap(grp(f).g), fact: f.fid, fixed: true, q: "Read both statements. I: " + st1 + " II: " + st2, c: opts, a: "ABCD"[right] + " · " + opts[right],
        e: "Statement I is " + (t1 ? "true" : "false") + ": " + sentence(f) + " Statement II is " + (t2 ? "true" : "false") + ": " + sentence(g), h: ["I:", "II:"] };
    },
    analogy: function (f) {
      var s = sibs(f).filter(function (x) { return x.s; });
      if (!f.s || !s.length) return null;
      var g = P(s), w = sibs(f).filter(function (x) { return x !== g && x.s; }).map(function (x) { return x.s; });
      if (w.length < 3) return null;
      return mcFrom(f.s, w, base(f, { q: g.t + " is to “" + g.s + "” as " + f.t + " is to ______.", a: f.s, e: sentence(g) + " " + sentence(f), h: [g.t, f.t] }));
    },
    pairs: function (f) {
      var s = shuffle(sibs(f).filter(function (x) { return x.s; })).slice(0, 3);
      if (!f.s || s.length < 3) return null;
      var right = f.t + " — " + f.s;
      var wrong = s.map(function (x, i) { return x.t + " — " + s[(i + 1) % 3].s; }); // rotate the cues so every pair is wrong
      return mcFrom(right, wrong, base(f, { q: "Which pair is correctly matched?", a: right, e: [f].concat(s).map(function (x) { return x.t + " → " + x.s; }).join(" · ") + ".", h: ["correctly matched"] }));
    },
    riddle: function (f) { // typed
      var clues = [f.pl ? "We are " + grp(f).gp + "." : "I am " + an(grp(f).g) + ".", f.pl ? "We " + f.d + "." : "I " + firstPerson(f.d) + "."];
      if (f.x) clues.push(f.x);
      var letters = f.t.replace(/[^A-Za-z]/g, "");
      clues.push((f.pl ? "Our" : "My") + " name starts with “" + letters.charAt(0).toUpperCase() + "” and has " + letters.length + " letters.");
      return base(f, { q: (f.pl ? "Who are we? " : "Who am I? ") + clues.join(" "), h: [grp(f).g] });
    }
  };
  var BY_LEVEL = {
    1: ["identify", "pickTerm", "pickTerm", "pickDesc", "trueFalse", "riddle"],
    2: ["pickTerm", "pickDesc", "trueFalse", "oddOne", "twoStatements", "analogy", "pairs", "identify", "riddle"],
    3: ["riddle", "twoStatements", "identify", "pairs", "oddOne", "analogy"]
  };

  function make(fid, level) {
    var f = ALLF.filter(function (x) { return x.fid === fid; })[0];
    var list = shuffle(BY_LEVEL[level] || BY_LEVEL[2]);
    for (var i = 0; i < list.length; i++) {
      var c = SHAPES[list[i]](f);
      if (c) { c.shape = list[i]; return c; }
    }
    return SHAPES.identify(f);
  }

  // ---------- register decks ----------
  window.GROUPS.splice(0, 0, { id: "topics", name: "Science topics · a different question every time", note: "Built from " + ALLF.length + " science facts. Each one can be asked 8 different ways, picked at random." });
  TOPICS.forEach(function (t) {
    window.DECKS.push({ id: t.id, group: "topics", name: t.name, round: "mix", pts: 2, time: 30 });
    window.CARDS[t.id] = ALLF.filter(function (f) { return grp(f).topic === t.id; }).map(function (f) {
      return { gen: "fact", fid: f.fid, cat: cap(grp(f).g), q: sentence(f), a: f.t, k: f.k, e: sentence(f) + (f.x ? " " + f.x : ""), h: [f.t] };
    });
  });
  window.FACTGEN = { make: make, count: ALLF.length, shapes: Object.keys(SHAPES), all: ALLF, SHAPES: SHAPES };
})();

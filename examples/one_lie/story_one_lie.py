"""Example: "In This World You Get One Lie" (version 1 look). Run: python story_one_lie.py <project folder>"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'lib'))
from story_lib import Story, project_dir_from_argv

S = Story("One Lie", "In a world where everyone gets one perfect lie, a son learns what his father used his on.")
S.cast = {
 "narrator":{"preset":"boy","shirt":"#d9622b","shirtDesign":"plain","pants":"#2b4fb8","hair":"short","hairColor":"#5a3a1e"},
 "dad":{"preset":"dad","shirt":"#7a4a2a","sleeves":"long","pants":"#2e2e3a","hair":"short","hairColor":"#8a8a8a"},
 "mom":{"preset":"mom","shirt":"#f2e6c9","hair":"long","hairColor":"#2a1a0e"},
 "jake":{"preset":"boy","shirtDesign":"tie","hair":"spiky","hairColor":"#e8c84a","shirt":"#9ec9f0","shirtDesign":"tie","accent":"#222222"},
 "boss":{"preset":"boss"},
 "aunt":{"preset":"grandma","shirt":"#d9a521","extras":["glasses"]},
 "landlord":{"preset":"worker","hair":"bald"},
}

# P1 hook
S.shot("plaza",["In this world,","you get one","*lie.*"],
 {"narrator":{"at":[-1,0,6.5],"expr":"smile","do":[{"do":"walk","at":0,"to":[-1,0,8.8],"dur":1.0}]}},
 {"on":"narrator","shot":"full","move":"push"}, extras={"walkers":6})
S.shot("plaza",["Whatever you say,","everyone believes it","*forever.*"],
 {"narrator":{"at":[-3,0,8.5],"expr":"talk","do":[{"do":"talk","at":0,"dur":1.5}]}},
 {"on":"crowd","shot":"wide","move":"pull"},
 extras={"crowd":{"n":14,"rows":2,"center":[0,0,12],"yaw":180,"spacing":2.6,"expr":"smile","do":[{"do":"nod","at":"believes","dur":1.6}]}})
S.shot("plaza",["Everyone except","*you.*"],
 {"narrator":{"at":[0,0,8.5],"expr":"nervous"}},
 {"on":"narrator","shot":"close","move":"push"},
 extras={"crowd":{"n":10,"rows":2,"center":[0,0,13],"yaw":180,"spacing":2.6,"expr":"smile","do":[{"do":"nod","at":0,"dur":1.6}]}},
 fx=[{"punch":0.15,"at":"you."}])
S.shot("plaza",["Most people","waste it."],
 {"narrator":{"at":[0,0,8.5],"expr":"smirk","do":[{"do":"shrug","at":"waste","dur":0.8}]}},
 {"on":"narrator","shot":"medium","from":"front-left","move":"push"})
# P2 Jake
S.shot("office",["My coworker","Jake told","our boss"],
 {"jake":{"spot":"desk2","expr":"grin"},"boss":{"spot":"cooler","face":"jake","expr":"blank"}},
 {"on":["jake","boss"],"shot":"wide","move":"push"})
S.shot("office",["he'd already","finished the","*report.*"],
 {"jake":{"spot":"center","face":"front","expr":"grin","hold":"paper","do":[{"do":"talk","at":0,"dur":1.8}]}},
 {"on":"jake","shot":"medium","move":"push"},fx=[{"sparkle":"jake","at":"report."}])
S.shot("office",["He hadn't","*started.*"],
 {"jake":{"spot":"desk2","expr":"nervous","do":[{"expr":"scared","at":"started."}]}},
 {"on":"jake","shot":"close","move":"push"},fx=[{"icon":"sweat","on":"jake","at":"started.","dur":1.0}])
S.shot("office",["Now our boss","quotes numbers"],
 {"boss":{"spot":"center","face":"front","expr":"proud","hold":"paper","do":[{"do":"talk","at":0,"dur":1.6}]}},
 {"on":"boss","shot":"medium","angle":"low","move":"push"})
S.shot("office",["from a report","that doesn't","*exist.*"],
 {"boss":{"at":[-2,0,6],"expr":"proud","do":[{"do":"talk","at":0,"dur":1.6}]},"jake":{"spot":"desk3","expr":"nervous"}},
 {"on":["boss","jake"],"shot":"wide","move":"pull"},fx=[{"icon":"question","on":"boss","at":"exist.","dur":1.0}])
# P3 Aunt
S.shot("street",["My aunt told","her landlord"],
 {"aunt":{"spot":"door","expr":"smile"},"landlord":{"spot":"sidewalk","face":"aunt","expr":"blank"}},
 {"on":["aunt","landlord"],"shot":"full","move":"push"})
S.shot("street",["the rent","was *paid.*"],
 {"landlord":{"spot":"center","face":"front","expr":"happy","do":[{"do":"nod","at":0,"dur":1.2}]}},
 {"on":"landlord","shot":"medium","move":"push"},fx=[{"stamp":"PAID!","at":"paid."}])
S.shot("living_room",["That was","eleven years","ago."],
 {"aunt":{"spot":"sofa","expr":"smirk","hold":"cup"}},
 {"on":"aunt","shot":"medium","move":"push"},fx=[{"title":"11 YEARS LATER","dur":1.2,"style":"banner","at":0}])
S.shot("living_room",["She still","hasn't *paid* it."],
 {"aunt":{"spot":"sofa","expr":"smirk","hold":"cup","do":[{"do":"eat","at":"hasn't","dur":1.2}]}},
 {"on":"aunt","shot":"medium","from":"front-right","move":"push"})
# P4 Dad
S.shot("living_room",["My dad","never used his."],
 {"dad":{"spot":"center","expr":"blank"}},
 {"on":"dad","shot":"medium","move":"push"})
S.shot("street",["Everyone said","he was","wasting it."],
 {"dad":{"spot":"sidewalk","expr":"blank"},"s1":{"at":[-3,0,7],"face":"dad","do":[{"do":"point","at":"said","dur":1.2}]},"s2":{"at":[-4.4,0,7],"face":"dad","expr":"smirk"}},
 {"on":["dad","s1","s2"],"shot":"wide","move":"push"})
S.shot("street",["He wore the","same coat","for nine winters,"],
 {"dad":{"at":[-4,0,8],"expr":"sleepy","do":[{"do":"walk","at":0,"to":[3,0,8],"dur":3.0}]}},
 {"on":"dad","shot":"full","move":"track-right"},mood="sunset")
S.shot("office",["worked","two jobs,"],
 {"dad":{"spot":"desk1","expr":"sleepy","do":[{"do":"type","at":0,"dur":2}]}},
 {"on":"dad","shot":"medium","move":"push"},fx=[{"icon":"clock","on":"dad","at":0.2,"dur":1.4}])
S.shot("living_room",["and every time","I asked","how he was,"],
 {"narrator":{"spot":"sofa","face":"dad","expr":"talk"},"dad":{"spot":"center","face":"narrator","expr":"sleepy"}},
 {"on":["narrator","dad"],"shot":"full","move":"push"})
S.shot("living_room",["he said","the same thing."],
 {"dad":{"spot":"center","expr":"smile"}},
 {"on":"dad","shot":"close","move":"push"})
S.shot("living_room",["*I'm fine.*"],
 {"dad":{"spot":"center","expr":"smile"}},
 {"on":"dad","shot":"extreme","move":"push","amount":0.15},fx=[{"punch":0.1,"at":0.1}])
# P5 begging
S.shot("living_room",["When I turned","eighteen,","I begged him."],
 {"narrator":{"spot":"center","expr":"sad","hold":"cake","do":[{"do":"talk","at":0,"dur":1.8}]},"dad":{"at":[2,0,6],"face":"narrator","expr":"blank"}},
 {"on":["narrator","dad"],"shot":"full","move":"push"})
S.shot("living_room",["Dad,","use your lie."],
 {"narrator":{"spot":"center","expr":"sad","do":[{"do":"talk","at":0,"dur":1.4}]}},
 {"on":"narrator","shot":"close","move":"push"})
S.shot("living_room",["Tell the world","we're rich."],
 {"narrator":{"spot":"center","expr":"happy","do":[{"do":"point","dir":"up","at":0,"dur":1.4}]}},
 {"on":"narrator","shot":"medium","move":"push"},props=[{"type":"money","at":[1.2,2.2,6.5]}])
S.shot("living_room",["He just laughed.","Not yet."],
 {"dad":{"spot":"center","expr":"laugh","do":[{"do":"laugh","at":0,"dur":1.4},{"expr":"smile","at":"Not"}]}},
 {"on":"dad","shot":"medium","move":"push"})
# P6 Mom
S.shot("bedroom",["Then Mom","got sick."],
 {"mom":{"at":[-2.5,0,-3.1],"base":"sit","seat":1.95,"face":"front","expr":"sad"}},
 {"on":"mom","shot":"medium","from":"front","move":"push"})
S.shot("bedroom",["He sat by her bed","every night."],
 {"dad":{"at":[-0.4,0,-1.2],"base":"sit","seat":1.38,"face":"mom","expr":"sad"},"mom":{"at":[-2.5,0,-3.1],"base":"sit","seat":1.95,"face":"front","expr":"sleepy"}},
 {"on":["dad","mom"],"shot":"wide","from":"front","move":"push"},mood="sunset")
S.shot("bedroom",["On the last night,","he held her hand"],
 {"dad":{"at":[-0.4,0,-1.2],"base":"sit","seat":1.38,"face":"mom","expr":"sad"},"mom":{"at":[-2.5,0,-3.1],"base":"sit","seat":1.95,"face":"front","expr":"sad"}},
 {"on":["dad","mom"],"shot":"wide","from":"front","move":"push"},mood="sunset")
S.shot("bedroom",["and whispered","something","I couldn't hear."],
 {"narrator":{"spot":"door","expr":"sad","do":[{"do":"look","at":0,"yaw":0.4,"dur":1.5}]}},
 {"on":"narrator","shot":"medium","move":"push"},mood="sunset",fx=[{"icon":"dots","on":"narrator","at":"something","dur":1.4}])
S.shot("bedroom",["She smiled.","Then she","fell asleep."],
 {"mom":{"at":[-2.5,0,-3.1],"base":"sit","seat":1.95,"face":"front","expr":"smile","do":[{"expr":"asleep","at":"fell"}]}},
 {"on":"mom","shot":"medium","from":"front","move":"push"},mood="sunset",fx=[{"icon":"zzz","on":"mom","at":"fell","dur":1.4}])
# P7 phone
S.shot("living_room",["Years later,","I found his old phone","in a drawer."],
 {"narrator":{"spot":"center","expr":"sad","hold":"phone"}},
 {"on":"narrator","shot":"medium","move":"push"},mood="sunset")
S.shot("living_room",["There was","one voice note."],
 {"narrator":{"spot":"sofa","expr":"sad","hold":"phone"}},
 {"on":"narrator","shot":"close","move":"push"},mood="night",fx=[{"icon":"note","on":"narrator","at":"voice","dur":1.4}])
S.shot("living_room",["I used my lie tonight.","I told her","I'd be okay."],
 {"narrator":{"spot":"sofa","expr":"sad","hold":"phone"}},
 {"on":"narrator","shot":"close","from":"front-left","move":"push"},mood="night")
S.shot("bedroom",["She *believed* it."],
 {"mom":{"at":[-2.5,0,-3.1],"base":"sit","seat":1.95,"face":"front","expr":"smile"}},
 {"on":"mom","shot":"medium","from":"front","move":"push"},mood="sunset",fx=[{"glint":"mom","at":"believed"}])
# P7 end
S.shot("street",["Everyone believes me."],
 {"dad":{"spot":"sidewalk","expr":"sad"}},
 {"on":"dad","shot":"wide","angle":"high","move":"push"},mood="night",extras={"walkers":8})
S.shot("street",["Everyone","except *me.*"],
 {"dad":{"spot":"sidewalk","expr":"sad"}},
 {"on":"dad","shot":"close","move":"push"},mood="night")
# P8
S.shot("living_room",["He has said","I'm fine","every day","for twenty years."],
 {"dad":{"spot":"door","face":"front","expr":"smile","do":[{"do":"wave","at":0,"dur":3.0}]}},
 {"on":"dad","shot":"medium","move":"track-right"},fx=[{"title":"20 YEARS","dur":1.0,"style":"banner","at":"twenty"}])
S.shot("living_room",["And I believed him."],
 {"narrator":{"spot":"center","expr":"smile","do":[{"expr":"sad","at":"him."}]}},
 {"on":"narrator","shot":"close","move":"push"})
S.shot("plaza",["Everyone did."],
 {"narrator":{"at":[1.5,0,8],"expr":"smile"},"dad":{"at":[-6,0,9],"expr":"sad"}},
 {"on":"establishing","shot":"wide","move":"push"} if False else {"on":["narrator","dad"],"shot":"wide","move":"push"},
 extras={"crowd":{"n":12,"rows":2,"center":[0,0,13],"yaw":180,"spacing":2.6,"expr":"happy"}})
S.shot("living_room",["Nobody","checked on him","once."],
 {"dad":{"spot":"sofa","expr":"sad"}},
 {"on":"dad","shot":"medium","move":"pull"},mood="night")
# P9
S.shot("street",["I'm calling him","right now."],
 {"narrator":{"spot":"sidewalk","expr":"nervous","hold":"phone","do":[{"do":"hold","at":0,"dur":1.8}]}},
 {"on":"narrator","shot":"close","move":"push"},mood="night")
S.shot("street",["If you got one lie,","who would you","tell it to?"],
 {"narrator":{"spot":"sidewalk","expr":"smile","hold":"phone"}},
 {"on":"narrator","shot":"medium","move":"push"},mood="night",
 fx=[{"glint":"narrator","at":"tell"}],out="fade")

S.save(project_dir_from_argv())

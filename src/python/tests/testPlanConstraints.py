from director.consoleapp import ConsoleApp
from director import robotsystem
from director import visualization as vis
from director import objectmodel as om
from director import ikplanner
from director import ikconstraintencoder as ce

import numpy as np
import pprint
import json


def getRobotState():
    return robotStateJointController.q.copy()


def buildConstraints():
    '''
    For testing, build some constraints and return them in a list.
    '''

    startPose = getRobotState()

    startPoseName = 'plan_start'
    endPoseName = 'plan_end'

    ikPlanner.addPose(startPose, startPoseName)
    ikPlanner.addPose(startPose, endPoseName)

    constraints = []
    constraints.extend(ikPlanner.createFixedFootConstraints(startPoseName))
    constraints.append(ikPlanner.createMovingBaseSafeLimitsConstraint())
    constraints.append(ikPlanner.createLockedLeftArmPostureConstraint(startPoseName))
    constraints.append(ikPlanner.createLockedRightArmPostureConstraint(startPoseName))
    constraints.append(ikPlanner.createLockedRightArmPostureConstraint(startPoseName))

    targetFrame = ikPlanner.getLinkFrameAtPose(ikPlanner.getHandLink('left'), startPose)

    p, o = ikPlanner.createPositionOrientationGraspConstraints('left', targetFrame)
    p.tspan = [1.0, 1.0]
    o.tspan = [1.0, 1.0]
    constraints.extend([p, o])

    return constraints



def testPlanConstraints():

    ikPlanner.planningMode = 'dummy'

    constraints = buildConstraints()
    poses = ce.getPlanPoses(constraints, ikPlanner)


    poseJsonStr = json.dumps(poses, indent=4)
    constraintsJsonStr = ce.encodeConstraints(constraints, indent=4)

    print poseJsonStr
    print constraintsJsonStr


    constraints = ce.decodeConstraints(constraintsJsonStr)
    pprint.pprint(constraints)



app = ConsoleApp()
app.setupGlobals(globals())

view = app.createView()
robotsystem.create(view, globals())


testPlanConstraints()

#app.start()

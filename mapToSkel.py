import vtk
import curvedSrep as cs
import matplotlib.pyplot as plt
def mapToSkel():
    for k in range(37,38):
        reader = vtk.vtkPolyDataReader()
        reader.SetFileName('control/bot_srep_twist' + str(k) + '.vtk')
        reader.Update()
        bot_srep = reader.GetOutput()

        reader2 = vtk.vtkPolyDataReader()
        reader2.SetFileName('control/FinTopMesh' + str(k) + '.vtk')
        reader2.Update()
        top_mesh = reader2.GetOutput()

        reader3 = vtk.vtkPolyDataReader()
        reader3.SetFileName('control/final_mesh/bot' + str(k) + '_label_SPHARM.vtk')
        reader3.Update()
        bot_mesh = reader3.GetOutput()

        num_pts = top_mesh.GetNumberOfPoints()
        implicit_distance = vtk.vtkImplicitPolyDataDistance()
        implicit_distance.SetInput(top_mesh)

        boundPts = vtk.vtkPoints()
        # prevPt = False
        for j in range(num_pts):
            pt = bot_mesh.GetPoint(j)
            dist = implicit_distance.FunctionValue(pt)
            if dist < 0.5:
                boundPts.InsertNextPoint([pt[0], pt[1], pt[2]])

        boundSet = vtk.vtkPolyData()
        boundSet.SetPoints(boundPts)
        boundSet.Modified()

        # writer = vtk.vtkPolyDataWriter()
        # writer.SetInputData(boundSet)
        # writer.SetFileName('boundPts.vtk')
        # writer.Write()

        testPts = vtk.vtkPoints()
        source_pts = vtk.vtkPoints()
        target_pts = vtk.vtkPoints()
        for i in range(bot_srep.GetNumberOfCells()):
            base_pt_id = i * 2
            bdry_pt_id = i * 2 + 1
            s_pt = bot_srep.GetPoint(base_pt_id)
            b_pt = bot_srep.GetPoint(bdry_pt_id)

            dist = implicit_distance.FunctionValue(b_pt)
            if dist < 0.5:
                source_pts.InsertNextPoint([b_pt[0], b_pt[1], b_pt[2]])
                target_pts.InsertNextPoint([s_pt[0], s_pt[1], s_pt[2]])
        source_pts.Modified()
        target_pts.Modified()

        # sSet = vtk.vtkPolyData()
        # sSet.SetPoints(source_pts)
        # sSet.Modified()

        # writer = vtk.vtkPolyDataWriter()
        # writer.SetInputData(sSet)
        # writer.SetFileName('sPts.vtk')
        # writer.Write()

        # tSet = vtk.vtkPolyData()
        # tSet.SetPoints(target_pts)
        # tSet.Modified()

        # writer2 = vtk.vtkPolyDataWriter()
        # writer2.SetInputData(tSet)
        # writer2.SetFileName('tPts.vtk')
        # writer2.Write()

        tps = vtk.vtkThinPlateSplineTransform()
        tps.SetSourceLandmarks(source_pts)
        tps.SetTargetLandmarks(target_pts)
        tps.SetBasisToR()
        tps.Modified()

        skelPts = vtk.vtkPoints()
        for i in range(0, boundSet.GetNumberOfPoints()):
            bPt = boundPts.GetPoint(i)
            sPt = tps.TransformPoint(bPt)

            skelPts.InsertNextPoint(sPt)
        skelSet = vtk.vtkPolyData()
        skelSet.SetPoints(skelPts)
        skelSet.Modified()

        rXs, rYs, rZs, rSamPts = cs.curvedSrep(skelSet)
        numSamp = len(rSamPts[0])

        plt.figure()
        ax = plt.subplot(111, projection='3d')

        tps2 = vtk.vtkThinPlateSplineTransform()
        tps2.SetSourceLandmarks(target_pts)
        tps2.SetTargetLandmarks(source_pts)
        tps2.SetBasisToR()
        tps2.Modified()

        # pt = target_pts.GetPoint(0)
        # newPt = tps2.TransformPoint([pt[0], pt[1], pt[2]])
        # onePts = vtk.vtkPoints()
        # onePts.InsertNextPoint([newPt[0], newPt[1], newPt[2]])
        # oneSet = vtk.vtkPolyData()
        # oneSet.SetPoints(onePts)
        # oneSet.Modified()
        # writer2 = vtk.vtkPolyDataWriter()
        # writer2.SetInputData(skelSet)
        # writer2.SetFileName('skelSet.vtk')
        # writer2.Write()


        iXs = []
        iYs = []
        iZs = []
        iSamPts = []
        srepPts = vtk.vtkPoints()
        pPts = vtk.vtkPoints()

        for i in range(0, len(rXs)):
            pPts.InsertNextPoint([rXs[i], rYs[i], rZs[i]])
            intPt = tps2.TransformPoint([rXs[i], rYs[i], rZs[i]])
            iXs.append(intPt[0])
            iYs.append(intPt[1])
            iZs.append(intPt[2])

            if i == 0:
                iSpoke = []
                srepPts.InsertNextPoint([iXs[i], iYs[i], iZs[i]])
                for j in range(0, numSamp):
                    intPt = tps2.TransformPoint(rSamPts[i][j])
                    iSpoke.append([intPt[0], intPt[1], intPt[2]])
                    srepPts.InsertNextPoint([intPt[0], intPt[1], intPt[2]])
                    ax.scatter(intPt[0], intPt[1], intPt[2], color='k')
                    if j == 0:
                        ax.plot([iXs[i], iSpoke[0][0]], [iYs[i], iSpoke[0][1]], [iZs[i], iSpoke[0][2]], 'r')
                    else:
                        ax.plot([iSpoke[j-1][0], iSpoke[j][0]], [iSpoke[j-1][1], iSpoke[j][1]], [iSpoke[j-1][2], iSpoke[j][2]], 'r')
                iSamPts.append(iSpoke)
            elif i == len(rXs)-1:
                iSpoke = []
                srepPts.InsertNextPoint([iXs[i], iYs[i], iZs[i]])
                for j in range(0, numSamp):
                    intPt = tps2.TransformPoint(rSamPts[-1][j])
                    iSpoke.append([intPt[0], intPt[1], intPt[2]])
                    srepPts.InsertNextPoint([intPt[0], intPt[1], intPt[2]])
                    ax.scatter(intPt[0], intPt[1], intPt[2], color='k')
                    if j == 0:
                        ax.plot([iXs[i], iSpoke[0][0]], [iYs[i], iSpoke[0][1]], [iZs[i], iSpoke[0][2]], 'r')
                    else:
                        ax.plot([iSpoke[j-1][0], iSpoke[j][0]], [iSpoke[j-1][1], iSpoke[j][1]], [iSpoke[j-1][2], iSpoke[j][2]], 'r')
                iSamPts.append(iSpoke)
            else:
                iSpoke = []
                srepPts.InsertNextPoint([iXs[i], iYs[i], iZs[i]])
                for j in range(0, numSamp):
                    intPt = tps2.TransformPoint(rSamPts[2*i-1][j])
                    iSpoke.append([intPt[0], intPt[1], intPt[2]])
                    srepPts.InsertNextPoint([intPt[0], intPt[1], intPt[2]])
                    ax.scatter(intPt[0], intPt[1], intPt[2], color='k')
                    if j == 0:
                        ax.plot([iXs[i], iSpoke[0][0]], [iYs[i], iSpoke[0][1]], [iZs[i], iSpoke[0][2]], 'r')
                    else:
                        ax.plot([iSpoke[j-1][0], iSpoke[j][0]], [iSpoke[j-1][1], iSpoke[j][1]], [iSpoke[j-1][2], iSpoke[j][2]], 'r')
                iSamPts.append(iSpoke)

                iSpoke = []
                srepPts.InsertNextPoint([iXs[i], iYs[i], iZs[i]])
                for j in range(0, numSamp):
                    intPt = tps2.TransformPoint(rSamPts[2*i][j])
                    iSpoke.append([intPt[0], intPt[1], intPt[2]])
                    srepPts.InsertNextPoint([intPt[0], intPt[1], intPt[2]])
                    ax.scatter(intPt[0], intPt[1], intPt[2], color='k')
                    if j == 0:
                        ax.plot([iXs[i], iSpoke[0][0]], [iYs[i], iSpoke[0][1]], [iZs[i], iSpoke[0][2]], 'r')
                    else:
                        ax.plot([iSpoke[j-1][0], iSpoke[j][0]], [iSpoke[j-1][1], iSpoke[j][1]], [iSpoke[j-1][2], iSpoke[j][2]], 'r')
                iSamPts.append(iSpoke)
        srepSet = vtk.vtkPolyData()
        srepSet.SetPoints(srepPts)
        srepSet.Modified()
        ax.plot(iXs, iYs, iZs, 'r')
        plt.show()
        writer2 = vtk.vtkPolyDataWriter()
        writer2.SetInputData(srepSet)
        writer2.SetFileName('control/2dsrep' + str(k) + '.vtk')
        writer2.Write()

    # pSet = vtk.vtkPolyData()
    # pSet.SetPoints(pPts)
    # pSet.Modified()
    # writer3 = vtk.vtkPolyDataWriter()
    # writer3.SetInputData(pSet)
    # writer3.SetFileName('psrep.vtk')
    # writer3.Write()


mapToSkel()
# writer2 = vtk.vtkPolyDataWriter()
# writer2.SetInputData(skelSet)
# writer2.SetFileName('skelProj.vtk')
# writer2.Write()

    

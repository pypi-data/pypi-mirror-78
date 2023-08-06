import numpy as np 

def vec_and_point_to_plane(vec, point):
    # ax + by + cz - d = 0
    return (*vec, np.dot(vec,point))

def cell2planes(cell):
    # 3 planes intersect the origin by ase design. 
    a = cell[0,:]
    b = cell[1,:]
    c = cell[2,:]
    print(cell)
    print(a)
    
    n1 = np.cross(a, b)
    n2 = np.cross(b, c)
    n3 = np.cross(c, a)

    origin = [0,0,0]
    top = a+b+c

    plane1 = vec_and_point_to_plane(n1, origin)
    plane2 = vec_and_point_to_plane(n2, origin)
    plane3 = vec_and_point_to_plane(n3, origin)
    plane4 = vec_and_point_to_plane(-n1, top)
    plane5 = vec_and_point_to_plane(-n2, top)
    plane6 = vec_and_point_to_plane(-n3, top)

    return [plane2, plane2, plane3, plane4, plane5, plane6]



if __name__ == "__main__":
    from molecular_builder import create_bulk_crystal
    atoms = create_bulk_crystal("alpha_quartz", size=(30,30,30))
    cell = atoms.cell
    print(cell)
    planes = cell2planes(cell)
    print(planes)
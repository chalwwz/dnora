import sys

# =============================================================================
# IMPORT dnora
# =============================================================================
dnora_directory = '../'
sys.path.insert(0, dnora_directory)
from dnora import grd, bnd, wnd, inp, run

# =============================================================================
# DEFINE GRID OBJECT
# =============================================================================

# Set grid definitions
lon_min = 4.5
lat_min = 60.83
lon_max = 5.5
lat_max = 61.25
grid = grd.Grid(lon_min, lon_max, lat_min, lat_max, name='Skjerjehamn')

# Set spacing and boundary points
grid.set_spacing(nx=55, ny=50)

bnd_set = grd.boundary.EdgesAsBoundary(edges=['N', 'W', 'S'], step=1)
#grid.set_boundary(bounN=1, edges=['N', 'W', 'S'])
grid.set_boundary(boundary_setter=bnd_set)

# Import topography and mesh it down to the grid definitions
grid.import_topo(topo_reader=grd.read.EMODNET2018(tile='D5'))
grid.mesh_grid()


# =============================================================================
# DEFINE BOUNDARY OBJECT
# =============================================================================

# Initialize boundary object with the grid
boundary = bnd.Boundary(grid, name='WAM4km')

# Fetch the boundary spectra
time0 = '2021-08-15T00:00'
time1 = '2021-08-17T00:00'
#boundary.import_boundary(start_time=time0, end_time=time1, boundary_reader=bnd.read.MetNo_WAM4km(ignore_nan=True), point_picker=bnd.pick.NearestGridPoint())

# =============================================================================
# DEFINE WIND FORCING OBJECT
# =============================================================================

forcing = wnd.Forcing(grid, name='MEPS')

# # Fetch the wind forcing
forcing.import_forcing(start_time=time0, end_time=time1, forcing_reader=wnd.read.MetNo_MEPS(prefix='det', stride=3, last_file='2021-08-16T00:00', hours_per_file=67))


# =============================================================================
# WRITE OUTPUT FOR SWAN RUN
# =============================================================================
output_folder = 'example_forecast'
# Grid
write_grid = grd.write.SWAN(folder=output_folder)
write_grid(grid)

# Boundary
write_boundary = bnd.write.SWAN(folder=output_folder)
write_boundary(boundary)

# Wind forcing
write_forcing = wnd.write.SWAN(folder=output_folder)
write_forcing(forcing)

# Write input file for SWAN model run
swan_directory = output_folder
write_input_file = inp.SWANInputFile(grid=grid, forcing=forcing)
input_file_name = write_input_file(
    start_time=time0, end_time=time1, swan_directory=swan_directory, wind=True)


# =============================================================================
# SWAN RUN
# =============================================================================
#run.run_SWAN(input_file_name, swan_directory=swan_directory)

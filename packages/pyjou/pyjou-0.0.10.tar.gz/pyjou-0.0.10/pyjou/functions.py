''' SET FUNCTIONS '''
yn = {
	True: 'yes',
	False: 'no'
}

def key_not_found(*args):
	print('Invalid keys or not enough input arguments.\nThe following keyword arguments must be defined: {}\n'.format(', '.join(args)))

''' FILE SECTION '''
def read_case(overwrite=True, **kwargs):
	try:
		return '/file/read-case "{}" {} '.\
			format(kwargs['path'], yn.get(overwrite))
	except KeyError:
		key_not_found('path')
		raise

def read_journal(**kwargs):
	try:
		path = kwargs['path']
		if type(path) == str:
			path = [path]
		return '/file/read-journal\n{}'.\
			format('\n'.join(path))
	except KeyError:
		key_not_found('path')
		raise

def write_case(overwrite=True, **kwargs):
	try:
		return '/file/write-case "{}" {} '.\
			format(kwargs['path'], yn.get(overwrite))
	except KeyError:
		key_not_found('path')
		raise

def write_case_data(overwrite=True, **kwargs):
	try:
		return '/file/write-case-data "{}" {} '.\
			format(kwargs['path'], yn.get(overwrite))
	except KeyError:
		key_not_found('path')
		raise

def mesh_replace(discard=True, **kwargs):
	try:
		return '/file/replace-mesh "{}" {} '.\
			format(kwargs['path'], yn.get(discard))
	except KeyError:
		key_not_found('path')
		raise

''' DEFINE SECTION '''
def bc_velocity_inlet(**kwargs):
	try:
		return '/define/boundary-conditions velocity-inlet {} no yes yes no 0 no {} no 0 no {} no no no yes 5 0.01 '.\
				format(kwargs['name'], kwargs['velocity'], kwargs['temperature'])
	except KeyError:
		key_not_found('name', 'velocity', 'temperature')
		raise

def bc_pressure_outlet(**kwargs):
	try:
		return '/define/boundary-conditions/pressure-outlet {} yes no 0. no {} no yes no no n yes 5. 0.01 yes no no no '.\
			format(kwargs['name'], kwargs['temperature'])
	except KeyError:
		key_not_found('name', 'temperature')
		raise

def bc_wall(fluid=True, **kwargs):
	try:
		if fluid:
			return '/define/boundary-conditions/wall {} 0. no 0. no yes temperature no {} no no no 0. no 0. no 1 '.\
				format(kwargs['name'], kwargs['temperature'])
		else:
			return '/define/boundary-conditions/wall {} 0. no 0. no yes temperature no {} no 1 '.\
				format(kwargs['name'], kwargs['temperature'])
	except KeyError:
		key_not_found('name', 'temperature')
		raise

def viscous(**kwargs):
	try:
		return '/define/models/viscous/{} yes '.\
			format(kwargs['model'])
	except KeyError:
		key_not_found('model')
		raise

''' SURFACE SECTION '''
def line_surface(**kwargs):
	try:
		return '/surface/line-surface {} {} {} {} {}'.\
			format(kwargs['name'], kwargs['x1'], kwargs['y1'], kwargs['x2'], kwargs['y2'])
	except KeyError:
		key_not_found('name', 'x1', 'y1', 'x2', 'y2')
		raise


def point_surface(**kwargs):
	try:
		return '/surface/point-surface {} {} {}'.\
			format(kwargs['name'], kwargs['x'], kwargs['y'])
	except KeyError:
		key_not_found('name', 'x', 'y')
		raise

''' MESH SECTION '''
def translate(**kwargs):
	try:
		return '/mesh/translate {} {} '.\
			format(kwargs['x'], kwargs['y'])
	except KeyError:
		key_not_found('x', 'y')
		raise

def append_mesh(**kwargs):
	try:
		return '/mesh/modify-zones/append-mesh "{}" '.\
			format(kwargs['path'])
	except KeyError:
		key_not_found('path')
		raise

def merge_zones(**kwargs):
	try:
		list_zones = kwargs['list_zones']
		try:
			list_zones[1]
		except [TypeError, IndexError]:
			print('"list_zones" should be a list of at least 2 zones')
			raise  
		return '/mesh/modify-zones/merge-zones {} () '.\
			format(' '.join(list_zones))
	except KeyError:
		key_not_found('list_zones')
		raise

def fuse_face_zones(fused_name='()', **kwargs):
	try:
		list_zones = kwargs['list_zones']
		try:
			list_zones[1]
		except [TypeError, IndexError]:
			print('"list_zones" must be a list of at least 2 zones')
			raise
		return '/mesh/modify-zones/fuse-face-zones {} () delete-me '.\
			format(' '.join(list_zones), fused_name)
	except KeyError:
		key_not_found('list_zones')
		raise

def zone_name(**kwargs):
	try:
		return '/mesh/modify-zones/zone-name {} {} '.\
			format(kwargs['old_name'], kwargs['new_name'])
	except KeyError:
		key_not_found('old_name', 'new_name')
		raise

def check():
	return '/mesh/check '
	
def repair():
	return '/mesh/repair-improve/repair '

''' SOLVE SECTION '''
def convergence_criteria(**kwargs):
	try:
		criteria = [str(x) for x in kwargs['criteria']]
		return '/solve/monitors/residual convergence-criteria {}'.\
			format(' '.join(criteria))
	except KeyError:
		key_not_found('criteria')
		raise

def cd_velocity_inlet(**kwargs):
	try:
		return '/solve/initialize/compute-defaults/velocity-inlet {} '.\
			format(kwargs['name'])
	except KeyError:
		key_not_found('name')
		raise

def initialize_flow():
	return '/solve/initialize initialize-flow yes '

def iterate(**kwargs):
	try:
		return '/solve/iterate {} '.\
			format(int(kwargs['iters']))
	except KeyError:
		key_not_found('iters')
		raise

''' REPORT SECTION '''
def mass_flow(all_zones=True, **kwargs):
	try:
		if all_zones:
			return '/report/fluxes/mass-flow yes yes "{}" yes '.\
				format(kwargs['path'])
		else:
			list_zones = kwargs['list_zones']
			try:
				list_zones[0]
			except IndexError:
				print('"list_zones" must be at least one name, but none is given')
				raise
			if type(list_zones) == str:
				list_zones = [list_zones]
			return '/report/fluxes/mass-flow no {} () yes "{}" yes '.\
				format(' '.join(list_zones), kwargs['path'])
	except KeyError:
		key_not_found('path', 'list_zones')
		raise

def heat_transfer(all_zones=True, **kwargs):
	try:
		if all_zones:
			return '/report/fluxes/heat-transfer yes yes "{}" yes '.\
				format(kwargs['path'])
		else:
			list_zones = kwargs['list_zones']
			try:
				list_zones[0]
			except IndexError:
				print('"list_zones" must be at least one name, but none is given')
				raise
			if type(list_zones) == str:
				list_zones = [list_zones]
			return '/report/fluxes/heat-transfer no {} () yes "{}" yes '.\
				format(' '.join(list_zones), kwargs['path'])
	except KeyError:
		key_not_found('path', 'list_zones')
		raise

def area(**kwargs):
	try:
		list_zones = kwargs['list_zones']
		try:
			list_zones[0]
		except IndexError:
			print('"list_zones" must be at least one name, but none is given')
			raise
		if type(list_zones) == str:
			list_zones = [list_zones]
		return '/report/surface-integrals/area {} () yes "{}" yes '.\
			format(' '.join(list_zones), kwargs['path'])
	except KeyError:
		key_not_found('path', 'list_zones')
		raise

def facet_avg(**kwargs):
	try:
		list_zones = kwargs['list_zones']
		try:
			list_zones[0]
		except IndexError:
			print('"list_zones" must be at least one name, but none is given')
			raise
		if type(list_zones) == str:
			list_zones = [list_zones]
		return '/report/surface-integrals/facet-avg {} () {} yes "{}" y '.\
			format(' '.join(list_zones), kwargs['value'], kwargs['path'])
	except KeyError:
		key_not_found('path', 'value', 'list_zones')
		raise

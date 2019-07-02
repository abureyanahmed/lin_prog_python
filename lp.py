from scipy.optimize import linprog

def get_objective(line):
  arr = line.split()
  res = []
  for i in range(0, len(arr), 2):
    if arr[i][0]=='+' or arr[i][0]=='-':
      num = float(arr[i][1:])
    else:
      num = float(arr[i])
    if arr[i][0]=='-':
      num = -num
    res.append(num)
  return res

def get_less_than_inequality(line, n_vars):
  arr = line.split()
  res = []
  prev_var = -1
  for i in range(0, len(arr)-2, 2):
    cur_var = int(arr[i+1].split('_')[1])
    for j in range(cur_var-prev_var-1):
      res.append(0)
    if arr[i][0]=='+' or arr[i][0]=='-':
      num = float(arr[i][1:])
    else:
      num = float(arr[i])
    if arr[i][0]=='-':
      num = -num
    res.append(num)
    prev_var = cur_var
  for j in range(n_vars-len(res)):
    res.append(0)

  i = len(arr)-1
  if arr[i][0]=='+' or arr[i][0]=='-':
    num = float(arr[i][1:])
  else:
    num = float(arr[i])
  if arr[i][0]=='-':
    num = -num

  return res, num

def read_model(file_name):
  print('Reading model.... All equations must be in less than equal to form')
  c = []
  A = []
  b = []
  f = open(file_name, 'r')
  line = f.readline().strip()
  maximize = False
  while line!='':
    #print(line)
    while line[0]=='#':
      line = f.readline().strip()
    if line=='maximize:' or line=='minimize:':
      type='objective'
      if line=='maximize:':
        maximize = True
    elif line=='subject to:':
      type='constraints'
    else:
      if type=='objective':
        c = get_objective(line)
        if maximize:
          c = convert_min_to_max(c)
      elif type=='constraints':
        coeff, cons = get_less_than_inequality(line, len(c))
        A.append(coeff)
        b.append(cons)
    line = f.readline().strip()
  f.close()
  return c, A, b

def convert_min_to_max(c):
  c = [-x for x in c]
  return c

def run_lin_prog(file_name):
  print('Running linear program')
  c, A, b = read_model(file_name)
  bounds = []
  for i in range(len(c)):
    bounds.append((0, None))
  res = linprog(c, A_ub=A, b_ub=b, bounds=bounds)
  print(res)

#run_lin_prog('simple.txt')
run_lin_prog('farmer.txt')


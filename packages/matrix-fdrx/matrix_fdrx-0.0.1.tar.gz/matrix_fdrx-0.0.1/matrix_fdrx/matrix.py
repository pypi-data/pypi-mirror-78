class Matrix:
    
    def __init__(self, nums, nrows, ncols, max_prec=5):
        assert len(nums) == nrows * ncols
        self.max_prec = max(0, max_prec)
        self.vals = [round(num, self.max_prec) for num in nums]
        self.nrows = nrows
        self.ncols = ncols

       
    def get_rows(self):
        return [self.vals[x:x+ncols] for x in range(nrows//ncols)]
    
    def get_cols(self):
        return [self.vals[x::nrows] for x in range(ncols)]
    
    def __add__(self, other):
        assert self.nrows == other.nrows and self.ncols == other.ncols
        return Matrix([u + v for u, v in zip(self.vals, other.vals)], self.nrows, self.ncols)
    
    def __sub__(self, other):
        assert self.nrows == other.nrows and self.ncols == other.ncols
        return Matrix([u - v for u, v in zip(self.vals, other.vals)], self.nrows, self.ncols)
    
    def __mul__(self, other):
        assert self.ncols == self.nrows
        nrows, ncols = self.nrows, other.ncols
        self_as_rows = self.get_rows()
        other_as_cols = other.get_cols()
        vals = list()
        for i in range(nrows):
            for j in range(ncols):
                vals.append( sum(u * v for u, v in zip(self_as_rows, other_as_cols)) )
        return Matrix(vals, nrows, ncols, min(self.max_prec, other.max_prec)
    
    def __repr__(self):
        max_tenz = max( round(math.log10(abs(vals)), 0) )
        max_tenz = int(max_tenz)
        max_chars = 1 + max_tenz + 1 + 1 + self.max_prec
        repr_vals = [[f'%+0{max_chars}.{self.max_prec}f' % vr for vr in row] for row in self.get_rows()]
        return '\n'.join([' | '.join(row_repr) for row_repr in repr_vals])
        
                      
        
           
        
                
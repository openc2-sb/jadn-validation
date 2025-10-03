class SignedInteger:
    
    data: any = None
    bits: int = None


    def __init__(self, data: any = None, bits: int = None):
        self.data = data
        self.bits = bits
    
    def validate(self):

        
        signed_value = int(self.bits) -1
        #print("iN value must be between - and + 2^("+str(self.bits)+"-1)-1")
        sig_min = pow(-2,signed_value)
        sig_max = pow(2,signed_value) -1

        if sig_min <= self.data <= sig_max:
            pass
        else:
            raise ValueError(f"Data {self.data} is out of range for a signed integer of {self.bits} bits.")


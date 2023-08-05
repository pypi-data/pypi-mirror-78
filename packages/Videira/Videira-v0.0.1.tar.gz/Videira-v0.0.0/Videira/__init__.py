# Author: OakAnderson(andersonfelipe01@live.com)
# Author: ZauJulio(zauhdf@gmail.com)
#
# Present...
####################################################### 
#                                                     #
# \\\\\\\\\\\\\\\\\\\ Jabuticaba //////////////////// #
#                                                     #
#######################################################


class Cacho:
    def __init__(self, uva):
        """ Cacho Classification

        Parameters
        ----------
        uva: dict

        Returns
        -------
        Cacho class with uva keys as attributes

        """
        if isinstance(uva, dict):
            self.__dict__ = uva
            for item in uva.keys():
                self.__dict__[item] = self.__reconstructor(self.__dict__[item])

    def __reconstructor(self, uva):
        """
        Parameters
        ----------
        uva: dict or any object

        Returns
        -------
        Cacho class if uva is a dict, otherwise return uva object
        """
        if isinstance(uva, dict):
            return Cacho(uva)

        return uva


if __name__ == "__main__":
    foo = { 'a':[1,2,3], 'b': {'c': 2} }
    
    bar = Cacho(foo)
    
    print(bar)
    print(bar.a)
    print(bar.a.b.c)

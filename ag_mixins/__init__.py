'''
The term "mixin" is commonly used in object-oriented programming to describe a 
class that provides functionality to be inherited by a subclass. In Python, 
mixins are often used to encapsulate reusable behavior that can be shared among 
different classes.

The key concept here is code reuse and encapsulation of common functionality in 
a separate class, which can be inherited by other classes as needed.
'''

from django.shortcuts import get_object_or_404 


class AgObjectRetrievalMixin:
    """
    Mixin class providing common methods for retrieving objects.
    """

    def ag_get_object_by_id(self, model, pk):
        """
        Retrieve the object by its primary key.

        Args:
            model (Model): The model class to retrieve the object from.
            pk (int): The primary key of the object.

        Returns:
            Model: The retrieved object.

        Raises:
            Http404: If the object with the given primary key does not exist.
        """

        # Using 'get_object_or_404', otherwise it throws 500 (Internal Server Error). 
        # get_object_or_404 provides a more user-friendly response when a 
        # requested object cannot be found, instead of displaying a server error page.

        return get_object_or_404(model, id=pk)
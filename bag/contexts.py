# the function is taking request as a parameter and will return
# a dictionary called context
def bag_contents(request):
    # This is known as a context processor,its purpose is to make
    # this dictionary available to all templates across the entire
    # application, like you can use request.user in any template
    # due to the presence of the built-in request context processor
    context = {}

    return context


from IPython.core.magic import register_line_cell_magic
@register_line_cell_magic
def doc(line:str=None, cell:str=None):
    """
    This Jupyter Magic automatically documents code when it's in the first line of a cell.

    Usage:
    ```
    import bia_bob
    ```
    ```
    %%document
    ... code you would like do document better
    ```
    """
    from ._machinery import Context, init_assistant, combine_user_input
    from ._utilities import generate_response_to_user
    from IPython.core.getipython import get_ipython

    code = combine_user_input(line, cell)

    prompt = f"""
    Please write comments in the following code.
    Put comments on new lines before the code block you describe. 
    If there are functions in the code, add numpy-style docstrings.
    
    ```python
    {code}
    ```
    """

    if Context.assistant is None:
        init_assistant()
    p = get_ipython()
    Context.variables = p.user_ns

    code, text = generate_response_to_user(Context.assistant.model, prompt)

    p.set_next_input(code, replace=True)



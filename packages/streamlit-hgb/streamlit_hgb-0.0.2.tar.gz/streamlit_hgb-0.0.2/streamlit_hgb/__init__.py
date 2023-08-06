import os
import streamlit as st
import streamlit.components.v1 as components
import socket
from contextlib import closing
import subprocess
import time
import yaml
import tempfile
from PIL import Image

def find_free_port(host):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind((host, 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = True

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
    host = os.environ.get("STREAMLIT_HOST", "localhost")
    _component_func = components.declare_component(
        # We give the component a simple, descriptive name ("my_component"
        # does not fit this bill, so please choose something better for your
        # own component :)
        "hgb",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://{}:3001".format(host),
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("hgb", path=build_dir)

# Retrieve samples from yaml file
@st.cache()
def load_samples(yaml_file):
    with open(yaml_file, "r") as f:
        y = yaml.load(stream=f, Loader=yaml.SafeLoader)
        return y

# Retrieve reference name and length from bam/ghb
@st.cache()
def reference_hash(name):
    """Calculate length of reference chromosomes.

    Parameters
    ----------
    name: str,
        A file name of BAM file to calculate.

    Returns
    -------
    hash
        Key: chromosome id, value: reference length.

    """

    if name == "":
        return {}
    binary = os.environ.get("HGB_BIN", "hgb")
    if name.endswith(".ghb"):
        param = "decompose -f {}".format(name)
    else:
        param = "split -f {}".format(name)
    cmd = [binary, *param.split()]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    hash = {}
    for line in proc.stdout.split("\n"):
        line = line.rstrip().split()
        if len(line) > 1:
            hash[line[0]] = int(line[1])
    return hash

def hgb_run(name, ref_id, range, coverage=None, opts="", split=False, y=32, callet=False, hide_ins=False, no_pack=False):
    """Create a single image by "hgb".

    Parameters
    ----------
    name: str,
        A file name to display.
    ref_id: str,
        A chromosome id to display.
    range: range,
        A genomic range.
    coverge: None or int,
        A height of alignment view. 
    opts: str,
        An optional option to pass hgb vis commands.
    split: True or False,
        Display split alignments in the same line.
    y: int,
        The height of each read alignment.
    callet: True or False,
        Show callets on ends of read alignments if the read contains translocationial split-alignment.
    hide_ins: True or False,
        Hide insertion callets on read alignments.
    no_pack: True or False,
        Disable read packing.

    Returns
    -------
    image
        A single image.
    """

    binary = os.environ.get("HGB_BIN", "hgb")
    fp = tempfile.NamedTemporaryFile(suffix=".png")
    param = "-t 2 vis -P -a {} -y {} -S -r {}:{}-{} -o {} {}".format(" ".join(name), y, ref_id, range[0], range[1], fp.name, opts)
    if split:
      param += " -s -u"
    if callet:
      param += " -e -T"
    if hide_ins:
      param += " -I"
    if no_pack:
      param += " -p"
    if coverage:
      param += " -m {}".format(coverage)
    cmd = [binary, *param.split()]
    print(" ".join(cmd))
    complete_process = subprocess.run(cmd, check=True)
     
    return Image.open(fp.name)

#@st.cache()
def hgb(name, ref_id, range, coverage, opts="", split=False, y=32, callet=False, hide_ins=False, no_pack=False):
    """Create a new instance of "hgb".

    Parameters
    ----------
    name: str,
        A file name to display.
    ref_id: str,
        A chromosome id to display.
    range: range,
        A genomic range.
    opts: str,
        An optional option to pass hgb vis commands.
    split: True or False,
        Display split alignments in the same line.
    y: int,
        The height of each read alignment.
    callet: True or False,
        Show callets on ends of read alignments if the read contains translocationial split-alignment.
    hide_ins: True or False,
        Hide insertion callets on read alignments.
    no_pack: True or False,
        Disable read packing.

    Returns
    -------
    ref_id, range, component
        The legend of annotations.

    """

    host = os.environ.get("STREAMLIT_HOST", "localhost")
    port = find_free_port(host)
    binary = os.environ.get("HGB_BIN", "hgb")
    offset = 100 * 1000
    cache_start = range[0] - offset if range[0] - offset > 1 else 1
    min_span = 10
    span = int((range[1]-range[0])/100)
    
    exact_end = (span if span > min_span else min_span) + range[0]
    param = "-t 2 vis -M 2048 -X 512 -Y 1024 -P -a {} -y {} -S -w {}:{} -r {}:{}-{} -R {}:{}-{} -Q -m {} {}".format(" ".join(name), y, host, port, ref_id, range[0], exact_end, ref_id, cache_start, range[1] + offset, coverage, opts)
    ppm = exact_end - range[0]
    if split:
      param += " -s -u"
    if callet:
      param += " -e -T"
    if hide_ins:
      param += " -I"
    if no_pack:
      param += " -p"
    cmd = ["nohup", binary, *param.split()]
    print(" ".join(cmd))
    
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    line = proc.stdout.readline()
    for line in proc.stdout:
        line = line.decode().rstrip()
        if (line).startswith("Server is running"):
            component_value = _component_func(host=host, port=port, ppm=ppm,default={})
            return ref_id, range, component_value

    # We could modify the value returned from the component if we wanted.
    # There's no need to do this in our simple example - but it's an option.
    return ref_id, range


# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run my_component/__init__.py`
if not _RELEASE:
    import streamlit as st

    st.header("Hybrid Genome Browser")

    # Create a second instance of our component whose `name` arg will vary
    # based on a text_input widget.
    #
    # We use the special "key" argument to assign a fixed identity to this
    # component instance. By default, when a component's arguments change,
    # it is considered a new instance and will be re-mounted on the frontend
    # and lose its current state. In this case, we want to vary the component's
    # "name" argument without having it get recreated.
    # name_input = st.text_input("Enter a file name", value="../../bt142/ont2_ngmlr.bam")
    try:
        yaml = load_samples("hgb/config.yaml")

        ref = st.sidebar.selectbox("Which references to use?", list(yaml.keys()) ,1)

        name_input = st.sidebar.multiselect("Which files to load?",
          yaml[ref]["samples"],
          list(yaml[ref]["default"])
        )
        refs = reference_hash(yaml[ref]["samples"][0]) 
        default_range = yaml[ref]["range"][0]
    except:    
        name_input = st.sidebar.text_input("Which file to explore?")
        refs = reference_hash(name_input)
        if len(refs) > 0:
            default_range = "{}:1-10001".format(next(iter(refs)))
        else:
            default_range = ""
    
    #range_candidate = st.sidebar
    region = st.sidebar.text_input("Where to explore?", default_range) #yaml[ref]["range"][0])
    split=False
    coverage=50
    y=64
    callet=True
    no_ins=False

    if len(refs) > 0:
        chr_def, region_chr = region.split(":")
        car, cdr = region_chr.split("-")
        chr = list(refs.keys())

        ref_id = st.sidebar.selectbox(
        'Which chromosome to display?',
        chr, chr.index(chr_def))
        range = st.sidebar.slider(
         'Select a range of values',
         0, refs[ref_id], (int(car), int(cdr)))


        if st.sidebar.checkbox("Detail"):
            num = st.sidebar.number_input("Enter a start coordinate", 0, refs[ref_id], range[0])
            num2 = st.sidebar.number_input("Enter a stop coordinate", 0, refs[ref_id], range[1])
            coverage = st.sidebar.number_input('The expected coverage', 1, 500, coverage)
            split = st.sidebar.checkbox('Split-alignment only view')
            callet = st.sidebar.checkbox('Show callets only intra-chromosomal split alignment', True)
            y = st.sidebar.number_input("Set a read height", 8, 128, y)

        if range[1] - range[0] <= 1000*1000*12:
            num_clicks = hgb(name_input, ref_id, range, coverage, split, y, callet)

    st.markdown(
        f"""
<style>
    .reportview-container .main .block-container{{
        max-width: 1280px;
    }}
</style>
""",
        unsafe_allow_html=True,
    )


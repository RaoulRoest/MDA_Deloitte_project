import os
import sys 
generalPath = os.path.join(os.path.dirname(__file__), "..", "General")
sys.path.append(generalPath)

import matplotlib.pyplot as plt

# Custom modules
from PathUtilities import make_directory_if_not_exists
from PathUtilities import check_extension

def get_default_plot_directory():
    curDir = os.path.dirname(__file__)
    return os.path.join(curDir, "Export", "Plot")

def get_plot_directory(subdirectoryName=None):
    defaultDir = get_default_plot_directory()
    
    if(subdirectoryName != None):
        plotDir = os.path.join(defaultDir, subdirectoryName)
    else:
        plotDir = defaultDir
        
    make_directory_if_not_exists(plotDir)
    return plotDir
    
def save_plot(fig, filename, identifier=None):
    plotDir = get_plot_directory(identifier)
    filePath = os.path.join(plotDir, filename)
    filePath = check_extension(filePath, "png")
    
    fig.savefig(filePath)

def set_plot_params(ax, title, xlabel, ylabel=None, legend=False):
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    
    if(not (ylabel is None)):
        ax.set_ylabel(ylabel)
    
    if(legend):
        ax.legend(loc="upper right", bbox_to_anchor=(1.05, 1))

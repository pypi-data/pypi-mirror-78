import cProfile, pstats, io, os
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import seaborn as sns
import pandas as pd

fontP = FontProperties()
fontP.set_size('small')

def remove_empty(l):
    """Removes all empty strings from a list

    Args:
        l (list): List containing strings

    Returns:
        list: List with empty strings removed
    """
    while "" in l: l.remove("")
    return l

def to_float(n):
    try:
        return float(n)
    except:
        return n

class Profiler:
    def __init__(self, dfs={}):
        self.dfs = dfs
        self.data = {}
        self.gotData = len(dfs) > 0
        self.count = len(dfs)
        self.name = ""
        self.names_count = {}

    def set_cprofiler(self, name=""):
        """Instances a cProfile to use inside code, user should use enable and disable methods
        of cProfile object to control the profiler, after the execution finished call stop to
        store results.

        Args:
            name (str, optional): Key of the execution, if none will be stored the count of
                executions. If not informed will assume "exec n" where n is the count of start()
                calls.

        Returns:
            cProfile: cProfile object.
        """
        # If no execution name given generates one based on the count of executions
        if name == "":
            name = "exec {:}".format(self.count)
        # Stores name and instances and return cProfile
        self.name = name
        self.profiler = cProfile.Profile()
        return self.profiler

    def start(self, name=""):
        """Instances and enables a cProfile object and starts profiling immediately.

        Args:
            name (str, optional):  Name of the execution, if none will be stored the count of
                executions. Defaults to "".

        Raises:
            ValueError: An invalid name was informed.
        """
        # If no execution name given generates one based on the count of executions
        if name == "":
            name = "exec{:03d}".format(self.count)
        if "_" in name:
            raise ValueError("Underscores are not allowed on execution names.")
        # Stores name and enables cProfile
        self.name = name
        self.profiler = cProfile.Profile()
        self.profiler.enable()

    def stop(self):
        """Disables cProfile object, parse and stores results of current execution.

        Raises:
            RuntimeWarning: User should not call stop without calling start() or set_cprofiler().
        """
        if self.name == "":
            raise RuntimeWarning('Must call start() before stop()!')
        else:
            # Disables cProfile and stores results in a string
            self.profiler.disable()
            s = io.StringIO()
            sortby = pstats.SortKey.CUMULATIVE
            ps = pstats.Stats(self.profiler, stream=s).sort_stats(sortby)
            ps.print_stats()
            # check if alreay executed with this name
            if not self.name in self.names_count:
                self.names_count[self.name] = 0
            # Get results headers
            results = remove_empty(s.getvalue().split('\n')[4:])
            headers = remove_empty(results[0].split(" "))
            headers[2] = headers[2]+"_"+headers[1]
            headers[4] = headers[4]+"_"+headers[3]
            headers[5] = 'function'
            # Parse data
            results = results[1:]
            data = {}
            for header in headers:
                data[header] = []
            for result in results:
                # Split every line with spaces and remove empty strings from resulting list
                line = remove_empty(result.split(" "))
                # Stores respective columns in data
                for i in range(len(headers)):
                    data[headers[i]].append(to_float(line[i]))
                # If line is bigger than headers, function name has spaces, append all excess items to function name
                if len(line) > len(headers):
                    for i in range(len(headers), len(line)):
                        data[headers[-1]][-1] = data[headers[-1]][-1] + " " + line[i]
            # Add extra keys to treat function name
            data['filename'] = []
            data['direc'] = []
            data['line'] = []
            data['short_name'] = []
            for i in range(len(data['function'])):
                # Standard function name: filename:lineno(function)
                if ":" in data['function'][i] and \
                    "(" in data['function'][i] and \
                    ")"  in data['function'][i]:
                    filename = data['function'][i][:-1].split(":")[0]
                    if "\\" in filename or "/" in filename:
                        direc, filename = os.path.split(filename)
                    else:
                        direc = ""
                    line = data['function'][i][:-1].split(":")[-1].split("(")[0]
                    function = data['function'][i][:-1].split(":")[-1].split("(")[1]
                    name = function+":"+line+"("+filename+")"
                # Method of imported objects: {method 'name' of 'class' objects}
                elif "{method" in data['function'][i]:
                    function = data['function'][i][:-1].split("'")[1]
                    filename = data['function'][i][:-1].split("'")[3]
                    name = function+"("+filename+")"
                    direc = ""
                    line = ""
                # Method of built-in objects: {built-in method class.method}
                elif "{built-in method" in data['function'][i]:
                    function = data['function'][i][:-1].split(" ")[2].split(".")[-1]
                    filename = data['function'][i][:-1].split(" ")[2].split(".")[:-1]
                    name = data['function'][i][:-1].split(" ")[2]
                    direc = ""
                    line = ""
                # If no match to any above just copy it
                else:
                    function = data['function'][i]
                    name = data['function'][i]
                    filename = ""
                    direc = ""
                    line = ""
                # Store parsed names to data
                data['function'][i] = function
                data['filename'].append(filename)
                data['direc'].append(direc)
                data['line'].append(line)
                data['short_name'].append(name)
                data['execution_id'] = self.names_count[self.name]
                data['execution_name'] = self.name
            # Creates a dataFrame with data and append to dfs list
            df = pd.DataFrame.from_dict(data)
            tottime = df[df.execution_id == self.names_count[self.name]].tottime.sum()
            df["tottime_perc"] = (df.tottime/tottime)*100
            df["cumtime_perc"] = (df.cumtime/tottime)*100
            if not self.name in self.dfs:
                self.dfs[self.name] = df
            else:
                self.dfs[self.name] = pd.concat([self.dfs[self.name], df], ignore_index=True)
            self.names_count[self.name] += 1
            self.gotData = True
            self.count += 1
            self.name = ""
            del self.profiler

    def list_execution_names(self):
        """Returns a list of all execution names stored in the object.

        Returns:
            list: Execution names.
        """
        dfs = self.results()
        return list(dfs.keys())

    def results(self):
        """Returns a dict with all executions dataframes.

        Raises:
            RuntimeWarning: There is no data stored.

        Returns:
            dict: Dict with results dataframes.
        """
        if self.gotData:
            return self.dfs
        else:
            raise RuntimeWarning('Called results before disable')

    def save_results(self, direc, prefix):
        """Saves data in csv files.

        Args:
            direc (string): Directory where results will be stored.
            prefix (string): Prefix name for the files.
        """
        dfs = self.results()
        if os.path.isdir(direc) == False:
                os.makedirs(direc)
        out = os.path.join(direc, prefix)
        for key in dfs.keys():
            dfs[key].to_csv(out+"_{:}.csv".format(key))

    def load_results(self, direc, prefix):
        """Load results from csv files.

        Args:
            direc (string): Directory where results are stored.
            prefix (string): Prefix name for the files.

        Raises:
            IOError: Failed to open one or more files.
        """
        # get list of files in direc
        try:
            all_files = list(os.walk(direc))[0][2]
        except:
            print("Could not find files in the specified directory.")
            return None
        csv_files = []
        for f in all_files:
            extension = f.split(".")[-1].lower()
            f_prefix = "_".join(f.split(".")[-2].split("_")[:-1]).lower()
            if extension == "csv" and f_prefix == prefix.lower():
                filename = os.path.join(direc, f)
                key = f.split(".")[-2].split("_")[-1]
                csv_files.append((key, filename))
        csv_files.sort(key=lambda x: int(x[0]))
        self.gotData = True
        for key, f in csv_files:
            try:
                df = pd.read_csv(f)
                self.dfs[key] = df
                exec_colunm = df["execution_id"].to_list()
                eid = []
                for i in exec_colunm:
                    if not i in eid:
                        eid.append(i)
                self.names_count[key] = len(eid)
            except:
                self.gotData = False
                self.dfs = {}
                raise IOError("Couldn't load file: {}, aborting.".format(f))

    def get_top_df(self, keys, n, time, functions=[]):
        dfs = self.results()
        if functions == []:
            for key in keys:
                for i in range(0, self.names_count[key]):
                    sorted_df = dfs[key][dfs[key].execution_id == i].sort_values(time, ascending=False)[:n]
                    try:
                        newdf = pd.concat([newdf, sorted_df])
                    except:
                        newdf = sorted_df
        else:
            for key in keys:
                for i in range(0, self.names_count[key]):
                    df = dfs[key][dfs[key].execution_id == i]
                    for j in range(len(functions)):
                        # Try to load results with exact match to function name
                        lines = df.loc[df.function == functions[j]]
                        # If unable to select a line by exact match try the first line that contais the function name
                        if lines.function.count() == 0:
                            lines = df.loc[df.function.str.contains(functions[j])]
                        # If successful in selecting a line
                        if lines.function.count() >= 1:
                            try:
                                newdf = pd.concat([newdf, lines.iloc[:1]])
                            except:
                                newdf = lines.iloc[:1].copy()
        newdf.reset_index(drop=True, inplace=True)
        return newdf

    def check_time(self, time):
        if not time.lower() in ["tottime", "cumtime"]:
            raise ValueError("{} is not a valid time, use tottime or cumtime.")

    def plot_top_time(self, filename=False, time="cumtime", keys=None, title="", n=10, size=(5, 4)):
        """Plots a bar plot for all given keys with the top n functions.

        Args:
            filename (bool, optional): File to store plot. If false no file will be saved, use `plt.show()` to see plot.
            time (str, optional): Cumulative time ("cumtime") or total time ("tottime") to plot. Defaults to "cumtime".
            keys (list, optional): List of execution keys to be ploted, if none is passed will plot all keys.
            title (bool, optional): Plot title. If not informed no title will be drawn.
            n (int, optional): Number of functions to plot if not given list of functions. Defaults to 10.
            size (tuple, optional): Size of the plot, tuple of floats in inches. Defaults to (5, 4).

        Raises:
            RuntimeWarning: User tried to plot without data.
            ValueError: `time` is not `cumtime` or `tottime`.
        """
        if keys == None:
            keys = self.list_execution_names()
        for key in keys:
            plt.figure(figsize=size)
            df = self.get_top_df([key], n, time)
            ax = sns.barplot(x="function", y=time, data=df, ci="sd", capsize=0.2, errwidth=1)
            ax.set_xlabel("Function")
            if time == "cumtime":
                ax.set_ylabel("Cumulative time (s)")
            elif time == "tottime":
                ax.set_ylabel("Total time (s)")
            else:
                ax.set_ylabel("time (s)")
            plt.title(title+key+" ("+time+")")
            plt.xticks(rotation=45, horizontalalignment='right')
            if filename:
                plt.savefig(filename+"_"+time+"_"+key+".pdf")

    def plot_function(self, functions=[], n=10, filename=False, keys=None, time="cumtime", percent=False, 
                      title=False, legend_outside=False, log=False, xlabel="Execution label", size=(5, 4)):
        """Plot the time in each function, by default plots the cumulative time for the top 10 functions

        Args:
            functions (list, optional): Functions to plot, if none given will plot top n functions.
            n (int, optional): Number of functions to plot if not given list of functions. Defaults to 10.
            filename (bool, optional): File to store plot.  If false no file will be saved, use `plt.show()` to see plot.
            keys (list, optional): List of execution keys to be ploted, if none is passed will plot all keys.
            time (str, optional): Cumulative time ("cumtime") or total time ("tottime") to plot. Defaults to "cumtime".
            percent (bool, optional): Plot values as percent instead of seconds. Defaults to False.
            title (bool, optional): Plot title. If not informed no title will be drawn.
            legend_outside (bool, optional): Puts the legend ouside the plot. Defaults to False.
            log (bool, optional): (Experimental) Try to plot in log-log scale (x values must be equaly spaced).
            xlabel (str, optional): Label for the x axis.
            size (tuple, optional): Size of the plot, tuple of floats in inches. Defaults to (5, 4).
        Raises:
            RuntimeWarning: User tried to plot without data.
            ValueError: `time` is not `cumtime` or `tottime`.
        """
        # Get data
        if keys == None:
            keys = self.list_execution_names()
        df = self.get_top_df(keys, n, time, functions)
        # Start plot
        plt.figure(figsize=size)
        self.check_time(time)
        if percent:
            time += "_perc"
        ax = sns.lineplot(x="execution_name", y=time.lower(), hue="function",data=df)
        # Try to convert xticks to number
        # try:
        #     x = [float(key) for key in keys]
        #     plt.xticks(x)
        # except:
        plt.xticks(rotation=45)
        if log:
            try:
                plt.xscale("log")
                plt.yscale("log")
            except:
                pass
        # If got title as parameter print it
        if title:
            plt.title(title)
        # Generates y label
        if "cumtime" in time:
            yLabel = "Cumulative time"
        elif "tottime" in time:
            yLabel = "Total time"
        else:
            yLabel = time + " time"
        if percent:
            yLabel = yLabel + " (%)"
        else:
            yLabel = yLabel + " (s)"
        # Print labels
        ax = plt.gca()
        ax.set_xlabel(xlabel)
        ax.set_ylabel(yLabel)
        # Print legend according to parameters
        if legend_outside:
            plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.tight_layout(pad=0.5)
        # Given fimename saves pdf
        if filename:
            plt.savefig(filename)
        return df
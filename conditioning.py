import numpy as np
from matplotlib import pyplot as plt

class RescorlaWagnerModel():
    def __init__(self):
        self.conditioned_stimuli = np.array([])
        self.conditioned_stimuli = np.array([])
        self.unconditioned_stimuli = np.array([])
        self.acquisition_phases = np.array([])
        self.extinction_phases = np.array([])
        self.association_strength = np.array([])
        self.ntrials = 0

    def add_conditioned_stimulus(self, saliance, name=''):
        stimulus = {
            'id' : len(self.conditioned_stimuli),
            'saliance' : saliance,
            'name' : name
        }
        self.conditioned_stimuli = np.append(self.conditioned_stimuli, stimulus)

    def add_unconditioned_stimulus(self, saliance, name=''):
        stimulus = {
            'id' : len(self.unconditioned_stimuli),
            'saliance' : saliance,
            'name' : name
        }
        self.unconditioned_stimuli = np.append(self.unconditioned_stimuli, stimulus)
        n, m = len(self.conditioned_stimuli), len(self.unconditioned_stimuli)
        if n > 0:
            if np.shape(self.association_strength) == (0,):
                self.association_strength = np.zeros(shape=(n,m))
            else:
                print('code has to be adapted!')

    def acquisition_phase(self, conditioned_stimuli_names, unconditioned_stimuli_names, n_trials=1):
        mask_conditioned = [(i['name'] in conditioned_stimuli_names) for i in self.conditioned_stimuli]
        mask_unconditioned = [(i['name'] in unconditioned_stimuli_names) for i in self.unconditioned_stimuli]
        acquisition = {
            'conditioned_stimuli' : self.conditioned_stimuli[mask_conditioned],
            'unconditioned_stimuli' : self.unconditioned_stimuli[mask_unconditioned],
            'n_trials' : n_trials
        }
        self.acquisition_phases = np.append(self.acquisition_phases, acquisition)
        # for each unconditioned stimuli
        us = self.unconditioned_stimuli[mask_unconditioned][0]
        for i in range(n_trials):
            if len(np.shape(self.association_strength)) > 2:
                association_strength_total = np.sum(self.association_strength[-1][mask_conditioned])
                association_strength_new = self.association_strength[-1]
            else:
                association_strength_total = np.sum(self.association_strength)
                association_strength_new = np.zeros(shape=(len(self.conditioned_stimuli),1))
            shape = self.association_strength.shape
            for cs in self.conditioned_stimuli[mask_conditioned]:
                if len(np.shape(self.association_strength)) > 2:
                    association_strength_old = self.association_strength[-1][cs['id']]
                else:
                    association_strength_old = self.association_strength[cs['id']]
                association_strength_new_cs = association_strength_old + cs['saliance'] * us['saliance'] * (1 - association_strength_total)
                association_strength_new[cs['id']] = association_strength_new_cs
            if len(shape) > 2:
                self.association_strength = np.concatenate(
                    (self.association_strength, [association_strength_new]))
            else:
                self.association_strength = np.stack([self.association_strength, association_strength_new])
            #for cs in self.conditioned_stimuli[np.logical_not(mask_conditioned)]:
            #    print([cs["name"]])
            #    self.extinction_phase([cs["name"]], us["name"])
            self.ntrials += 1

    def extinction_phase(self, conditioned_stimuli_names, unconditioned_stimuli_names, n_trials=1):
        mask_conditioned = [(i['name'] in conditioned_stimuli_names) for i in self.conditioned_stimuli]
        mask_unconditioned = [(i['name'] in unconditioned_stimuli_names) for i in self.unconditioned_stimuli]
        acquisition = {
            'conditioned_stimuli' : self.conditioned_stimuli[mask_conditioned],
            'unconditioned_stimuli' : self.unconditioned_stimuli[mask_unconditioned],
            'n_trials' : n_trials
        }
        self.acquisition_phases = np.append(self.acquisition_phases, acquisition)
        # for each unconditioned stimuli
        us = self.unconditioned_stimuli[mask_unconditioned][0]
        for i in range(n_trials):
            shape = self.association_strength.shape
            for cs in self.conditioned_stimuli[mask_conditioned]:
                if len(np.shape(self.association_strength)) > 2:
                    association_strength_old = self.association_strength[-1][cs['id']]
                    association_strength_new = self.association_strength[-1]
                else:
                    association_strength_old = self.association_strength[cs['id']]
                    association_strength_new = np.zeros(shape=(len(self.conditioned_stimuli),1))
                association_strength_new_cs = association_strength_old + cs['saliance'] * us['saliance'] * (0 - association_strength_old)
                association_strength_new[cs['id']] = association_strength_new_cs
            if len(shape) > 2:
                self.association_strength = np.concatenate(
                    (self.association_strength, [association_strength_new]))
            else:
                self.association_strength = np.stack([self.association_strength, association_strength_new])
            self.ntrials += 1


    def plot(self, label=None, loc_legend='best'):
        if self.ntrials == 0:
            print("Please use add_acquisition_phase() before plotting!")
        else:
            x = np.arange(0, self.ntrials+1, 1)
            for i in self.conditioned_stimuli:
                y = [j[i['id']] for j in self.association_strength]
                if len(np.unique(y))>1:
                    if label:
                        l = label
                    else:
                        l = i['name'] + " (Saliance = " + str(i['saliance']) + ")"
                    plt.plot(x, y, label=l)
            plt.legend(loc=loc_legend)
            plt.xlabel('Trials')
            plt.ylabel("Association strength to US " + self.unconditioned_stimuli[0]["name"] + " (Saliance = " + str(self.unconditioned_stimuli[0]['saliance']) + ")")

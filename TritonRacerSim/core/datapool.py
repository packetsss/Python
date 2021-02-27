from TritonRacerSim.components.component import Component

class DataPool:
    def __init__(self):
        self.pool = dict()

    def add(self, component=Component()):
        for data_name in component.step_inputs:
            self.pool[data_name] = None

        for data_name in component.step_outputs:
            self.pool[data_name] = None

    def get_inputs_for(self, component=Component()):
        inputs = [self.pool[data_name] for data_name in component.step_inputs]
        inputs = tuple(inputs)
        return inputs

    def store_outputs_for(self, component=Component(), output_values=None):
        current_idx = 0
        try:
            if output_values is not None:
                for i in range(len(component.step_outputs)):
                    current_idx = i
                    self.pool[component.step_outputs[i]] = output_values[i]
        except:
            print(f'Datapoll: error associated with {component.getName()} on storing output {current_idx + 1}')
            raise Exception()

    def get_value(self, name):
        return self.pool[name]

    def set_value(self, name, value):
        self.pool[name] = value
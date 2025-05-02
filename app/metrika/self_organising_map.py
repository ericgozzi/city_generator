import math
import random
import csv
import ast 

from pixels import Picture
from pixels import get_blank_picture
from pixels import add_centered_text
from pixels import create_grid_of_pictures

from pixels import Color


class SOM():

    """
    A Self Organising Map class.

    Attributes:
        grid_size (tuple): A tuple (x, y) representing the number of cells in x and y direction.
        input_dim (int): The dimensionality of the dataset.
        learning_rate (str): Learning rate value. 
        dataset (dict): A dictionary of the dataset containing a an object for the key and a list for the vector as data. 
    """

    
    def __init__(self, grid_size: tuple, input_dim: int, learning_rate: float, dataset: dict):
        self.grid_size = grid_size
        self.input_dim = input_dim 
        self.learning_rate = learning_rate 
        self.data = dataset
        self.weights: list = []
        self.radius = self.initial_radius
        self.global_magnitude = None

    @property
    def initial_radius(self):
        return max(self.grid_size)


    def __str__(self):
        return f"""
        SOM:
        ---
            Grid size (x,y):        {self.grid_size}
            Vector dimension:       {self.input_dim}
            Learning rate:          {self.learning_rate}
            Global magnitude:       {self.global_magnitude}
            Number of Items(data):  {len(self.data)}
        """



    def set_global_magnitude(self):
        """
        Calculates and set the global magnitude for the SOM.

        Parameters
        ----------
        None

        Returns
        ----------
        None
        """
        # Flatten all vectors and calculate the global Euclidean norm
        all_values = [x for values in self.data.values() for x in values]
        self.global_magnitude = math.sqrt(sum(x**2 for x in all_values))



    
    def normalize_item(self, item):
        """
        Normalize Item
        Normalize a new Item according to the normalization of the dataset
        """
        if not self.global_magnitude: return

        normalized_item = [x / self.global_magnitude for x in item]
        return normalized_item




    def normalize_data(self) -> None:
        """
        Normalize dataset vectors.

        Parameters
        ----------
        None

        Returns
        ----------
        None
        """
        # Normalize data
        if not self.global_magnitude: self.set_global_magnitude()

        # Normalize each vector using the global magnitude
        normalized_data = {
            key: [x / self.global_magnitude for x in value]
            for key, value in self.data.items()
        }
        self.data = normalized_data





    def initialize_neuron_weights(self) -> None:
        """ 
        Initialize the weights of the SOM neruon to random values.
        The random values are not normalized with the global magnitude.

        Parameters
        ----------
        None

        Returns
        ----------
        None
        """
        # Reset the weights
        self.reset_weights()

        # Add random weight to every cell
        for x in range(self.grid_size[0]):
            row = []
            for y in range(self.grid_size[1]):
                # Random weight vector for each neuron (within range [0, 1])
                w = [random.random() for _ in range(self.input_dim)]
                w = self.normalize_item(w)
                row.append(w)
            self.weights.append(row)
    




    def reset_radius(self) -> None:
        """
        Reset the radius value to the initial radius value.

        Parameters
        ----------
        None

        Returns
        ----------
        None
        """
        self.radius = self.initial_radius

    



    def reset_weights(self) -> None:
        """
        Reset the weights of the SOM neuron to an empty list. 

        Parameters
        ----------
        None

        Returns
        ----------
        None
        """
        self.weights = []





    def train(self, epochs: int) -> None:
        """
        Train the SOM.

        Parameters
        ----------
        epochs: int
            Nomber of training iterations the SOM will go thorough. 

        Returns
        ----------
        None
        """
        #self.radius = max(self.grid_size) / 2  # Initial radius of the neighborhood
        values = self.data.values()
        #self.initial_radius = self.radius
        for epoch in range(epochs):
            self.radius = self.initial_radius * (1 - (epoch / epochs))
            print(self.radius)
            for value in values:
                # Find the Best Matching Unit (BMU)
                bmu_idx = self.find_best_matching_unit(value)
                # Update the weights of the SOM
                self.update_weights(value, bmu_idx, epoch, epochs)
                #self.radius -= self.learning_rate





    def find_best_matching_unit(self, vector: list[float]) -> tuple:
        """
        Find the Best Matching Unit (BMU) on the current som neuron weights.

        Parameters
        ----------
        vector: list[float]
            Vector for whicht to find the BMU:

        Returns
        ----------
            bmu: tuple
                Tuple indicating the SOM coordinates of the BMU.
        """
        # Set infinity as minimum distance
        min_distance = float('inf')
        bmu = (0, 0)
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                # Calculate the Euclidean distance between input x and the neuron weight
                distance = self.euclidean_distance(self.weights[i][j], vector)
                if distance < min_distance:
                    min_distance = distance
                    bmu = (i, j)
        return bmu





    def update_weights(self, vector: list[float], bmu: tuple, epoch: int, epochs: int):
        """
        Update the weights of the SOM neurons.

        Parameters
        ----------
        vector: list[float]
            Vector of the datset that is updating the neighborhood.
        
        bmu:  tuple
            Bmu of the vector.

        epoch: int
            Current interation of the training porcess.

        epochs: int
            Total numeber of iterations.

        Returns
        ----------
        None
        """
        # Calculate the decay for learning rate and neighborhood size
        learning_rate = self.learning_rate * math.exp(-epoch / epochs)
        radius = self.radius * math.exp(-epoch / epochs)

        # Iterate over the grid and update weights based on their distance from BMU
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                # Calculate the distance from the BMU (Euclidean)
                distance = self.euclidean_distance([i, j], bmu)
                if distance <= radius:
                    # Update the weights with the neighborhood function
                    influence = self.neighborhood_function(distance, radius)
                    for k in range(self.input_dim):
                        self.weights[i][j][k] += influence * learning_rate * (vector[k] - self.weights[i][j][k])





    def euclidean_distance(self, v1: list, v2: list) -> float:
        """
        Calculate the euclidean distance between two vectors of n dimension

        Parameters
        ----------
        v1 : list[float]
            Vector 1.

        v2 : list[float]
            Vector 2.

        Returns
        ----------
        float
            The euclidean distance between the two vectors.

        """
        return math.sqrt(sum((v1[i] - v2[i]) ** 2 for i in range(len(v1))))
    




    def neighborhood_function(self, euclidean_distance: float, radius: float) -> float:
        """
        Calculate the result of the neighborood function.

        Parameters
        ----------
        euclidean_distance : float
            The euclidean distance bwtween a dataset vector and adn a som neuron. 

        radius : float
            Radius of influence of the neighborhood. 

        Returns
        ----------
        float
            The result of the neighborhood function.
        """
        return math.exp(-euclidean_distance**2 / (2 * (radius**2)))
    
    


    def get_weights_table(self):
        '''
        Get the weights of the neurons in a table format.

        Parameters
        ----------
        None    

        Returns
        ----------
        list
            A list of lists containing the weights of the neurons.
        '''
        tot_weights = []

        for i in range(self.grid_size[0]):
            row_weights = []

            for j in range(self.grid_size[1]):
                neuron = []

                for k in range(self.input_dim):
                    neuron.append(self.weights[i][j][k])
                
                row_weights.append(neuron)

            tot_weights.append(row_weights)

        return tot_weights





    def export_weights_as_csv(self, file_path: str, file_name: str) -> None:
        """
        Export the neuron weights as a csv file. 

        Parameters
        ----------
        file_path: str
            The file path on which export the csv file.

        Returns
        ----------
            None
        """
        file_name = file_name or "weights"

        # Create the filename
        file_path = file_path + file_name + ".csv"

        # Export the weights to a CSV file
        with open(file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(self.weights)




    def import_weights_from_csv(self, file_path: str) -> None:
        """
        Import the neuron weights from a csv file. 

        Parameters
        ----------
        file_path: str
            The path to the .csv file containig the weights. 

        Returns
        ----------
            None
        """
        
        # Reading the CSV file
        with open(file_path, mode="r") as file:
            reader = csv.reader(file)
            data = [[ast.literal_eval(cell) if cell.startswith("[") else cell for cell in row] for row in reader]
        print(data)
        self.weights = data





    def get_items_mapped(self):
        data_keys = self.data.keys()
        bmus = []
        for x in range(self.grid_size[0]):
            row = []
            for y in range(self.grid_size[1]):
                item = []
                for key in data_keys:
                    bmu = self.find_best_matching_unit(self.data[key])
                    if bmu[0] == x and bmu[1] == y:
                        item.append(key)
                row.append(item)
            bmus.append(row)
        return bmus
                




    def get_som_picture(self):

        items_mapped = self.get_items_mapped()
        flattened_list = []
        for x in range(self.grid_size[0]):
            for y in range(self.grid_size[1]):
                    flattened_list.append(', '.join(items_mapped[x][y]))

        squares = []
        for item in flattened_list:
            pic = get_blank_picture(512, 512, Color(255, 255, 255), 1)
            pic = add_centered_text(pic, item)
            squares.append(pic)

        table = create_grid_of_pictures(squares, grid_size=self.grid_size, image_size=(512, 512))

        return table




    




def remap_number(number: float, source_range: tuple, target_range: tuple) -> float:
    """
    Remaps a number from one range to another.

    Parameters:
    ----------
    number : float
        The number to remap
    source_range : tuple
        The range of the number
    target_range : tuple
        The target range of the number

    Returns:
    -------
    float
        The remapped number
    """
    source_start, source_end = source_range
    target_start, target_end = target_range
    source_range = source_end - source_start
    target_range = target_end - target_start
    return target_start + ((number - source_start) / source_range) * target_range








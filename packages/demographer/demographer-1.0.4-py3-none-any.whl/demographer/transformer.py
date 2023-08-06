import numpy as np


class Transformer():
  """A transformer is used to normalize our continuous features such as
    followers count, satuses count to a -1,1 range

  The transformer should have been created using train set, and later should be used on
  dev set and test set
  """
  def __init__(self, data, num_bins, from_dict=None):
    if from_dict is not None:
      assert data is None
      assert sorted(from_dict.keys()) == ['edges', 'histogram', 'max', 'min']

      for key, val in from_dict.items():
        if type(val) == list:
          val = np.array(val)
        setattr(self, key, val)

    else:
      self.min = np.min(data)
      self.max = np.max(data)
      self.histogram, self.edges = self.hist(data, num_bins)

  def to_dict(self):
    d = {'min': self.min, 'max': self.max,
         'histogram': self.histogram.tolist(),
         'edges': self.edges}
    return d

  def hist(self, data, num_bins):
    ptiles = [np.percentile(data, x)
              for x in np.arange(num_bins + 1) * (100 / num_bins)]
    return np.histogram(data, bins=ptiles, density=True)

  def within_bin_location(self, x, query_bin):
    left = self.edges[query_bin - 1]
    right = self.edges[query_bin]
    bin_density = (right - left) * self.histogram[query_bin - 1]
    return (x - left) / (right - left) * bin_density

  def left_edge_location(self, left_edge):
    loc = 0
    for i in range(int(left_edge)):
      density = self.histogram[i]
      width = self.edges[i + 1] - self.edges[i]
      loc += density * width

    return loc

  def transform(self, query):
    ''' Convert query into [-1, 1] normalized for data shape '''
    if query is None:
      return 0
    if query <= self.min:
      return -1
    if query >= self.max:
      return 1

    right_edge = np.digitize(query, self.edges)
    loc = self.left_edge_location(right_edge - 1)
    loc2 = self.within_bin_location(query, right_edge)
    output = -1 + 2 * (loc + loc2)
    return max(-1, min(1, output))

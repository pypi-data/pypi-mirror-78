### iSSVD - Intergrative Biclustering for Multi-view data with nested stability selection


_Inputs_:

 **X**: A list contains multi-view data.
 
 **standr**: If True each view will to be standardized. Default: False.
 
 **pointwise**: If True a fast pointwise control method will be performed for stability selection. Default: True.
 
 **steps**: Number of subsmaples used to perform stability selection. Default: 100.
 
 **size**: Size of the subsamples used to perform stability selection. Default: 0.5.
 
 **vthr**: The proportion to be explained by eigenvalues. Default: 0.7.
 
 **ssthr**: Range of the threshold for stability selection. Default: \[0.6, 0.8\].
 
 **nbicluster**: A user specified number of biclusters to be detected. Default: 10.
 
 **rows_nc**: If True allows for negative correlation of rows over columns. Default: True.
 
 **cols_nc**: If True allows for negative correlation of columns over rows. Default: True.
 
 **col_overlap**: If True allows for columns overlaps among biclusters. Default: False.
 
 **row_overlap**: If True allows for rows overlaps among biclusters. Default: False.
 
 **pceru**: Per-comparrison wise error rate to control the number of falsely selected coefficients in the left singular vectors. Default: 0.1.
 
 **pcerv**: Per-comparrison wise error rate to control the number of falsely selected coefficients in the right singular vector. Default: 0.1.
 
 **merr**: Convergence threshold. Default: 1e-4.
 
 **iters**: Maximal iteration for detecting each bicluster. Default: 100.
 
 
_Outputs_:

 iSSVD returns the stable solutions of left singular vectors for each bicluster, and right singular vectors from each view for each bicluster. 
 
 **N**: Number of biclusters detected.
 
 **Info**: Stability selection results of left and right singular vectors.
 
 **Sample_index**: The indices of bicluster samples.
 
 **Variable_index**: The indices of bicluster variables. 
 
 **Iterations:** The interations run for each bicluster.
 
 Please check https://github.com/weijie25/iSSVD/blob/master/iSSVD/Guide.md for a simple guide.



 *Reference*

 Weijie Zhang and Sandra E. Safo. "Robust Integrative Biclustering for Multi-view Data." *Bioinformatics* submitted (2020).

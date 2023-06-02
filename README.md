PyTexture is an exploration tool for microstructure data. Grain orientation data from a metallic 
microstructure (FCC or HCP) can be uploaded and various features can be extracted such as Schmid factors or 
Taylor factors. The addition of neighbor data can be used to extract grain-neighbor features
such as misorientations and slip transmission.

PyTexture can also be used to randomly generate grain orientations if no data exists. 

# Install
As this is currently in development, the best way to install this is via pip development mode.

1. Clone the directory.
2. Navigate to the directory.
3. Use:

```pip install --editable .```

4. Test that this was successful via:

```python -c 'import PyTexture'```

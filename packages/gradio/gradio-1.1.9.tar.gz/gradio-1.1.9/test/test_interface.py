import unittest
import numpy as np
import gradio as gr
import gradio.inputs
import gradio.outputs


class TestInterface(unittest.TestCase):
    def test_input_output_mapping(self):
        io = gr.Interface(inputs='sketchpad', outputs='text', fn=lambda x: x,
                          analytics_enabled=False)
        self.assertIsInstance(io.input_interfaces[0], gradio.inputs.Image)
        self.assertIsInstance(io.output_interfaces[0], gradio.outputs.Textbox)

    def test_input_interface_is_instance(self):
        inp = gradio.inputs.Image()
        io = gr.Interface(inputs=inp, outputs='text', fn=lambda x: x,
                          analytics_enabled=False)
        self.assertEqual(io.input_interfaces[0], inp)

    def test_output_interface_is_instance(self):
        out = gradio.outputs.Label()
        io = gr.Interface(inputs='sketchpad', outputs=out, fn=lambda x: x,
                          analytics_enabled=False)
        self.assertEqual(io.output_interfaces[0], out)

    def test_prediction(self):
        def model(x):
            return 2*x
        io = gr.Interface(inputs='textbox', outputs='text', fn=model,
                          analytics_enabled=False)
        self.assertEqual(io.predict[0](11), 22)


if __name__ == '__main__':
    unittest.main()
import glfw
import OpenGL.GL as gl
import numpy as np

# Shader sources
vertex_src = """
#version 330 core
layout (location = 0) in vec2 aPos;
void main()
{
    gl_Position = vec4(aPos.x, aPos.y, 0.0, 1.0);
}
"""

fragment_src = """
#version 330 core
out vec4 FragColor;

uniform float zoom;

void main()
{
    // Fractal rendering logic goes here
    vec2 coord = gl_FragCoord.xy;
    // The fractal rendering logic will depend on the zoom and the coordinates

    // Placeholder for fractal color based on pixel position
    FragColor = vec4(coord.x, coord.y, zoom, 1.0);
}
"""

# Initialize GLFW
if not glfw.init():
    raise Exception("glfw can not be initialized!")

# Set up GLFW window hints for macOS compatibility
glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)  # Required on Mac
glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)  # Requests core profile

# Now create the window
window = glfw.create_window(1280, 720, "3D Fractal Zoom", None, None)


# Create a window
window = glfw.create_window(1280, 720, "3D Fractal Zoom", None, None)

# Check if window was created
if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")

# Set window's position
glfw.set_window_pos(window, 400, 200)

# Make the context current
glfw.make_context_current(window)

# Compile and link shaders
shader_program = gl.glCreateProgram()
vertex_shader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
gl.glShaderSource(vertex_shader, vertex_src)
gl.glCompileShader(vertex_shader)
fragment_shader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
gl.glShaderSource(fragment_shader, fragment_src)
gl.glCompileShader(fragment_shader)

# Check for shader compile errors
if not gl.glGetShaderiv(vertex_shader, gl.GL_COMPILE_STATUS):
    raise RuntimeError(gl.glGetShaderInfoLog(vertex_shader).decode("utf-8"))
if not gl.glGetShaderiv(fragment_shader, gl.GL_COMPILE_STATUS):
    raise RuntimeError(gl.glGetShaderInfoLog(fragment_shader).decode("utf-8"))

gl.glAttachShader(shader_program, vertex_shader)
gl.glAttachShader(shader_program, fragment_shader)
gl.glLinkProgram(shader_program)

# Check for linking errors
if not gl.glGetProgramiv(shader_program, gl.GL_LINK_STATUS):
    raise RuntimeError(gl.glGetProgramInfoLog(shader_program).decode("utf-8"))

gl.glUseProgram(shader_program)

# Define and set up fullscreen quad vertices
quad_vertices = np.array([-1.0, -1.0, 1.0, -1.0, 1.0, 1.0, -1.0, 1.0], dtype=np.float32)
VBO = gl.glGenBuffers(1)
gl.glBindBuffer(gl.GL_ARRAY_BUFFER, VBO)
gl.glBufferData(
    gl.GL_ARRAY_BUFFER, quad_vertices.nbytes, quad_vertices, gl.GL_STATIC_DRAW
)
gl.glEnableVertexAttribArray(0)
gl.glVertexAttribPointer(0, 2, gl.GL_FLOAT, gl.GL_FALSE, 0, None)

# Get the uniform location for the zoom
zoom_location = gl.glGetUniformLocation(shader_program, "zoom")

# Main loop
while not glfw.window_should_close(window):
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    # Update zoom uniform
    zoom_value = 1  # your code to update the zoom effect over time
    gl.glUniform1f(zoom_location, zoom_value)

    # Draw quad
    gl.glDrawArrays(gl.GL_TRIANGLE_FAN, 0, 4)

    # Swap the front and back buffer
    glfw.swap_buffers(window)

    # Poll for and process events
    glfw.poll_events()

# Cleanup
gl.glDeleteShader(vertex_shader)
gl.glDeleteShader(fragment_shader)
gl.glDeleteProgram(shader_program)
glfw.terminate()

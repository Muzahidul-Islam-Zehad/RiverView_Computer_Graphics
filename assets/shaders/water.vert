#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aNormal;
layout (location = 2) in vec2 aTexCoords;

out vec3 FragPos;
out vec3 Normal;
out vec2 TexCoords;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform float time;

void main()
{
    // Wave animation - increased amplitude for more wavy appearance
    vec3 position = aPos;
    
    // Multiple wave patterns with increased amplitude
    float wave1 = sin(position.x * 3.0 + time * 1.5) * 0.08;      // Increased from 0.035
    float wave2 = cos(position.z * 2.0 + time * 1.0) * 0.06;      // Increased from 0.025
    float wave3 = sin(position.x * 5.0 + position.z * 3.0 + time * 2.0) * 0.04;  // Increased from 0.015
    float wave4 = cos(position.x * 1.5 + time * 0.8) * 0.05;      // New wave
    float wave5 = sin(position.z * 4.0 + time * 1.2) * 0.035;     // New wave
    
    float total_wave = wave1 + wave2 + wave3 + wave4 + wave5;
    position.y += total_wave;
    
    FragPos = vec3(model * vec4(position, 1.0));
    Normal = aNormal;
    TexCoords = aTexCoords;
    
    gl_Position = projection * view * vec4(FragPos, 1.0);
}
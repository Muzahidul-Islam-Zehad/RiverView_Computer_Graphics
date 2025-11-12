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
    // Realistic wave animation - only affect Y position
    vec3 position = aPos;
    
    // Multiple wave layers for realism
    float wave1 = sin(position.x * 3.0 + time * 1.5) * 0.02;
    float wave2 = cos(position.z * 2.0 + time * 1.0) * 0.015;
    float wave3 = sin(position.x * 5.0 + position.z * 3.0 + time * 2.0) * 0.01;
    
    // Combine waves with different frequencies
    position.y += wave1 + wave2 + wave3;
    
    // Calculate normal for lighting (approximate wave normal)
    vec3 normal = aNormal;
    normal.x += -cos(position.x * 3.0 + time * 1.5) * 0.1;
    normal.z += -sin(position.z * 2.0 + time * 1.0) * 0.08;
    normal = normalize(normal);
    
    FragPos = vec3(model * vec4(position, 1.0));
    Normal = normal;
    TexCoords = aTexCoords;
    
    gl_Position = projection * view * vec4(FragPos, 1.0);
}
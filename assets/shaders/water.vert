#version 330 core

layout(location = 0) in vec3 aPos;
layout(location = 1) in vec3 aNormal;
layout(location = 2) in vec2 aTexCoord;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform float time;

out vec3 vPos;
out vec3 vNormal;
out vec2 vTexCoord;

void main()
{
    // Wave animation: simple sine wave displacement
    vec3 pos = aPos;
    pos.y += sin(pos.x * 2.0 + time) * 0.05 + sin(pos.z * 2.0 + time * 0.8) * 0.05;
    
    vPos = vec3(model * vec4(pos, 1.0));
    vNormal = mat3(transpose(inverse(model))) * aNormal;
    vTexCoord = aTexCoord;
    gl_Position = projection * view * vec4(vPos, 1.0);
}

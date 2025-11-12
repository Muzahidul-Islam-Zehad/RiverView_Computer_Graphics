#version 330 core

in vec3 vPos;
in vec3 vNormal;
in vec2 vTexCoord;

out vec4 FragColor;

uniform sampler2D texture0;
uniform vec3 waterColor;
uniform vec3 lightPos;
uniform vec3 viewPos;
uniform float transparency;

void main()
{
    // Water with transparency and light reflection
    vec3 norm = normalize(vNormal);
    vec3 lightDir = normalize(lightPos - vPos);
    float diff = max(dot(norm, lightDir), 0.0);
    
    vec3 viewDir = normalize(viewPos - vPos);
    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 64.0);
    
    vec3 result = waterColor * (0.3 + diff * 0.7) + vec3(1.0) * spec * 0.8;
    
    FragColor = vec4(result, transparency);
}

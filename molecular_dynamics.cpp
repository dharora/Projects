#include <iostream>
#include <vector>
#include <cmath>
#include <fstream>
#include "matplotlibcpp.h"

namespace plt = matplotlibcpp;

struct Particle {
    double x, y, z;
    double vx, vy, vz;
    double ax, ay, az;
    double mass;

    Particle(double x, double y, double z, double vx, double vy, double vz, double mass)
        : x(x), y(y), z(z), vx(vx), vy(vy), vz(vz), ax(0.0), ay(0.0), az(0.0), mass(mass) {}
};

void calculateForce(const Particle& particleA, const Particle& particleB, double& fx, double& fy, double& fz) {
    const double G = 6.67430e-11;
    const double softeningFactor = 1e-10;

    double dx = particleB.x - particleA.x;
    double dy = particleB.y - particleA.y;
    double dz = particleB.z - particleA.z;
    double distanceSq = dx*dx + dy*dy + dz*dz + softeningFactor*softeningFactor;
    double distance = std::sqrt(distanceSq);

    double force = (G * particleA.mass * particleB.mass) / (distanceSq * distance);
    fx = force * dx;
    fy = force * dy;
    fz = force * dz;
}

void updateParticles(std::vector<Particle>& particles, double timestep) {
    const double dampingFactor = 0.99;

    size_t numParticles = particles.size();

    std::vector<double> ax(numParticles, 0.0);
    std::vector<double> ay(numParticles, 0.0);
    std::vector<double> az(numParticles, 0.0);

    for (size_t i = 0; i < numParticles; ++i) {
        for (size_t j = i + 1; j < numParticles; ++j) {
            Particle& particleA = particles[i];
            Particle& particleB = particles[j];

            double fx, fy, fz;
            calculateForce(particleA, particleB, fx, fy, fz);

            ax[i] += fx / particleA.mass;
            ay[i] += fy / particleA.mass;
            az[i] += fz / particleA.mass;
            ax[j] -= fx / particleB.mass;
            ay[j] -= fy / particleB.mass;
            az[j] -= fz / particleB.mass;
        }
    }

    for (size_t i = 0; i < numParticles; ++i) {
        Particle& particle = particles[i];

        particle.vx += ax[i] * timestep;
        particle.vy += ay[i] * timestep;
        particle.vz += az[i] * timestep;

        particle.x += particle.vx * timestep;
        particle.y += particle.vy * timestep;
        particle.z += particle.vz * timestep;

        particle.vx *= dampingFactor;
        particle.vy *= dampingFactor;
        particle.vz *= dampingFactor;
    }
}

void saveDataToCSV(const std::vector<std::vector<double>>& data, const std::string& filename) {
    std::ofstream file(filename);
    if (!file.is_open()) {
        std::cerr << "Error: Unable to open the file: " << filename << std::endl;
        return;
    }

    for (const auto& row : data) {
        for (size_t i = 0; i < row.size(); ++i) {
            file << row[i];
            if (i < row.size() - 1) {
                file << ",";
            }
        }
        file << "\n";
    }

    file.close();
}

void plotParticles(const std::vector<Particle>& particles) {
    std::vector<double> x, y, z;
    for (const auto& particle : particles) {
        x.push_back(particle.x);
        y.push_back(particle.y);
        z.push_back(particle.z);
    }

    plt::scatter(x, y);
    plt::title("Molecular Dynamics Simulation");
    plt::xlabel("X");
    plt::ylabel("Y");
    plt::show();
}

int main() {
    std::vector<Particle> particles;
    particles.emplace_back(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0);
    particles.emplace_back(1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0);

    double timestep = 0.01;
    int numSteps = 100;

    std::vector<std::vector<double>> positions;
    positions.reserve(numSteps);

    for (int step = 0; step < numSteps; ++step) {
        updateParticles(particles, timestep);

        std::vector<double> currentPositions;
        for (const auto& particle : particles) {
            currentPositions.push_back(particle.x);
            currentPositions.push_back(particle.y);
            currentPositions.push_back(particle.z);
        }
        positions.push_back(currentPositions);
    }

    // Output handling: Save data to CSV file
    saveDataToCSV(positions, "particle_positions.csv");

    // Visualization
    plotParticles(particles);

    return 0;
}

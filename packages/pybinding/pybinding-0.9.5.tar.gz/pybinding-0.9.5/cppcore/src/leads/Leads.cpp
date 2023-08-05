#include "leads/Leads.hpp"

namespace cpb {

void Leads::create_attachment_area(Foundation& foundation) const {
    for (auto const& spec : specs) {
        leads::create_attachment_area(foundation, spec);
    }
}

void Leads::make_structure(Foundation const& foundation) {
    if (!structures.empty()) {
        return;
    }

    for (auto const& spec : specs) {
        structures.emplace_back(foundation, spec);
    }
}

void Leads::make_hamiltonian(Lattice const& lattice, HamiltonianModifiers const& modifiers,
                             bool is_double, bool is_complex) {
    if (!hamiltonians.empty()) {
        return;
    }

    for (auto const& structure : structures) {
        hamiltonians.emplace_back(structure.system, lattice, modifiers, is_double, is_complex);
    }
}

void Leads::clear_structure() {
    structures.clear();
    clear_hamiltonian();
}

void Leads::clear_hamiltonian() {
    hamiltonians.clear();
}

} // namespace cpb

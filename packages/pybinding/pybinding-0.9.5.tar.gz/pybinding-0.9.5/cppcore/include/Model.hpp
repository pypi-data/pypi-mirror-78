#pragma once
#include "system/Registry.hpp"
#include "system/System.hpp"
#include "system/Shape.hpp"
#include "system/Symmetry.hpp"
#include "system/StructureModifiers.hpp"
#include "leads/Leads.hpp"
#include "hamiltonian/Hamiltonian.hpp"
#include "hamiltonian/HamiltonianModifiers.hpp"

#include "utils/Chrono.hpp"
#include "detail/sugar.hpp"

#include <string>
#include <vector>

namespace cpb {

class Model {
public:
    Model(Lattice const& lattice);

    /// The arguments can any type accepted by `Model::add()`
    template<class... Args>
    Model(Lattice const& lattice, Args&&... args) : Model(lattice) {
        detail::eval_ordered({(add(std::forward<Args>(args)), 0)...});
    }

public: // add parameters
    void add(Primitive primitive);
    void add(Shape const& shape);
    void add(TranslationalSymmetry const& s);

    void attach_lead(int direction, Shape const& shape);

    void add(SiteStateModifier const& m);
    void add(PositionModifier const& m);
    void add(OnsiteModifier const& m);
    void add(HoppingModifier const& m);

    void add(SiteGenerator const& g);
    void add(HoppingGenerator const& g);

    void set_wave_vector(Cartesian const& k);

public:
    /// Are any of the onsite or hopping energies given as matrices instead of scalars?
    bool is_multiorbital() const;
    /// Uses double precision values in the Hamiltonian matrix?
    bool is_double() const;
    /// Uses complex values in the Hamiltonian matrix?
    bool is_complex() const;

public: // get parameters
    Lattice const& get_lattice() const { return lattice; }
    SiteRegistry const& get_site_registry() const { return site_registry; }
    HoppingRegistry const& get_hopping_registry() const { return hopping_registry; }
    Primitive const& get_primitive() const { return primitive; }
    Shape const& get_shape() const { return shape; }
    TranslationalSymmetry const& get_symmetry() const { return symmetry; }

public: // get properties
    std::shared_ptr<System const> const& system() const;
    Hamiltonian const& hamiltonian() const;
    /// Return all leads
    Leads const& leads() const;
    /// Return lead at index
    Lead lead(size_t i) const { return leads()[i]; }

    /// The model properties listed above are usually evaluated lazily, only as needed.
    /// Calling this function will evaluate the entire model ahead of time. Always returns itself.
    Model const& eval() const;

public: // get information
    /// Report of the last build operation: system and Hamiltonian
    std::string report();
    double system_build_seconds() const { return system_build_time.elapsed_seconds(); }
    double hamiltonian_build_seconds() const { return hamiltonian_build_time.elapsed_seconds(); }

public:
    void clear_structure_modifiers() { structure_modifiers.clear(); }
    void clear_hamiltonian_modifiers() { hamiltonian_modifiers.clear(); }
    void clear_all_modifiers() { clear_structure_modifiers(); clear_hamiltonian_modifiers(); }

private:
    std::shared_ptr<System> make_system() const;
    Hamiltonian make_hamiltonian() const;

    /// Clear any existing structural data, implies clearing Hamiltonian
    void clear_structure();
    /// Clear Hamiltonian, but leave structural data untouched
    void clear_hamiltonian();

private:
    Lattice lattice;
    SiteRegistry site_registry;
    HoppingRegistry hopping_registry;

    Primitive primitive;
    Shape shape;
    TranslationalSymmetry symmetry;
    Cartesian wave_vector = {0, 0, 0};

    std::vector<StructureModifier> structure_modifiers;
    HamiltonianModifiers hamiltonian_modifiers;

    mutable std::shared_ptr<System const> _system;
    mutable Hamiltonian _hamiltonian;
    mutable Leads _leads;
    mutable Chrono system_build_time;
    mutable Chrono hamiltonian_build_time;
    mutable bool complex_override = false; ///< set if a modifier was found to (dynamically)
                                           ///< return complex output for real input data
};

} // namespace cpb

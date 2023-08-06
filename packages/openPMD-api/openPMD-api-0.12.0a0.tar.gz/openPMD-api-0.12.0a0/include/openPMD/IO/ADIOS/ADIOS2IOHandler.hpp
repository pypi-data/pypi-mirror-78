/* Copyright 2017-2020 Fabian Koller and Franz Poeschel
 *
 * This file is part of openPMD-api.
 *
 * openPMD-api is free software: you can redistribute it and/or modify
 * it under the terms of of either the GNU General Public License or
 * the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * openPMD-api is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License and the GNU Lesser General Public License
 * for more details.
 *
 * You should have received a copy of the GNU General Public License
 * and the GNU Lesser General Public License along with openPMD-api.
 * If not, see <http://www.gnu.org/licenses/>.
 */
#pragma once

#include "ADIOS2FilePosition.hpp"
#include "openPMD/config.hpp"
#include "openPMD/IO/AbstractIOHandler.hpp"
#include "openPMD/IO/AbstractIOHandlerImpl.hpp"
#include "openPMD/IO/AbstractIOHandlerImplCommon.hpp"
#include "openPMD/IO/IOTask.hpp"
#include "openPMD/IO/InvalidatableFile.hpp"
#include "openPMD/auxiliary/JSON.hpp"
#include "openPMD/backend/Writable.hpp"

#if openPMD_HAVE_ADIOS2
#   include <adios2.h>
#   include "openPMD/IO/ADIOS/ADIOS2Auxiliary.hpp"
#endif

#if openPMD_HAVE_MPI
#   include <mpi.h>
#endif

#include <nlohmann/json.hpp>

#include <array>
#include <exception>
#include <future>
#include <iostream>
#include <memory> // shared_ptr
#include <string>
#include <unordered_map>
#include <utility> // pair
#include <vector>

namespace openPMD
{
#if openPMD_HAVE_ADIOS2

class ADIOS2IOHandler;

namespace detail
{
    template < typename, typename > struct DatasetHelper;
    struct DatasetReader;
    struct AttributeReader;
    struct AttributeWriter;
    template < typename > struct AttributeTypes;
    struct DatasetOpener;
    template < typename > struct DatasetTypes;
    struct WriteDataset;
    struct BufferedActions;
    struct BufferedPut;
    struct BufferedGet;
    struct BufferedAttributeRead;
} // namespace detail


class ADIOS2IOHandlerImpl
: public AbstractIOHandlerImplCommon< ADIOS2FilePosition >
{
    template < typename, typename > friend struct detail::DatasetHelper;
    friend struct detail::DatasetReader;
    friend struct detail::AttributeReader;
    friend struct detail::AttributeWriter;
    template < typename > friend struct detail::AttributeTypes;
    friend struct detail::DatasetOpener;
    template < typename > friend struct detail::DatasetTypes;
    friend struct detail::WriteDataset;
    friend struct detail::BufferedActions;
    friend struct detail::BufferedAttributeRead;

    static constexpr bool ADIOS2_DEBUG_MODE = false;


public:

#if openPMD_HAVE_MPI

    ADIOS2IOHandlerImpl( AbstractIOHandler *, MPI_Comm, nlohmann::json config );

    MPI_Comm m_comm;

#endif // openPMD_HAVE_MPI

    explicit ADIOS2IOHandlerImpl(
        AbstractIOHandler *
        , nlohmann::json config
    );


    ~ADIOS2IOHandlerImpl( ) override = default;

    std::future< void > flush( ) override;

    void createFile( Writable *,
                     Parameter< Operation::CREATE_FILE > const & ) override;

    void createPath( Writable *,
                     Parameter< Operation::CREATE_PATH > const & ) override;

    void
    createDataset( Writable *,
                   Parameter< Operation::CREATE_DATASET > const & ) override;

    void
    extendDataset( Writable *,
                   Parameter< Operation::EXTEND_DATASET > const & ) override;

    void openFile( Writable *,
                   Parameter< Operation::OPEN_FILE > const & ) override;

    void closeFile( Writable *,
                    Parameter< Operation::CLOSE_FILE > const & ) override;

    void openPath( Writable *,
                   Parameter< Operation::OPEN_PATH > const & ) override;

    void openDataset( Writable *,
                      Parameter< Operation::OPEN_DATASET > & ) override;

    void deleteFile( Writable *,
                     Parameter< Operation::DELETE_FILE > const & ) override;

    void deletePath( Writable *,
                     Parameter< Operation::DELETE_PATH > const & ) override;

    void
    deleteDataset( Writable *,
                   Parameter< Operation::DELETE_DATASET > const & ) override;

    void deleteAttribute( Writable *,
                          Parameter< Operation::DELETE_ATT > const & ) override;

    void writeDataset( Writable *,
                       Parameter< Operation::WRITE_DATASET > const & ) override;

    void writeAttribute( Writable *,
                         Parameter< Operation::WRITE_ATT > const & ) override;

    void readDataset( Writable *,
                      Parameter< Operation::READ_DATASET > & ) override;

    void readAttribute( Writable *,
                        Parameter< Operation::READ_ATT > & ) override;

    void listPaths( Writable *, Parameter< Operation::LIST_PATHS > & ) override;

    void listDatasets( Writable *,
                       Parameter< Operation::LIST_DATASETS > & ) override;

    void
    listAttributes( Writable *,
                    Parameter< Operation::LIST_ATTS > & parameters ) override;

    /**
     * @brief The ADIOS2 access type to chose for Engines opened
     * within this instance.
     */
    adios2::Mode adios2AccessMode( );


private:
    adios2::ADIOS m_ADIOS;

    struct ParameterizedOperator
    {
        adios2::Operator const op;
        adios2::Params const params;
    };

    std::vector< ParameterizedOperator > defaultOperators;

    auxiliary::TracingJSON m_config;
    static auxiliary::TracingJSON nullvalue;

    void
    init( nlohmann::json config );

    template< typename Key >
    auxiliary::TracingJSON
    config( Key && key, auxiliary::TracingJSON & cfg )
    {
        if( cfg.json().is_object() && cfg.json().contains( key ) )
        {
            return cfg[ key ];
        }
        else
        {
            return nullvalue;
        }
    }

    template< typename Key >
    auxiliary::TracingJSON
    config( Key && key )
    {
        return config< Key >( std::forward< Key >( key ), m_config );
    }

    /**
     *
     * @param config The top-level of the ADIOS2 configuration JSON object
     * with operators to be found under dataset.operators
     * @return first parameter: the operators, second parameters: whether
     * operators have been configured
     */
    std::pair< std::vector< ParameterizedOperator >, bool >
    getOperators( auxiliary::TracingJSON config );

    // use m_config
    std::pair< std::vector< ParameterizedOperator >, bool >
    getOperators();

    /*
     * We need to give names to IO objects. These names are irrelevant
     * within this application, since:
     * 1) The name of the file written to is decided by the opened Engine's
     *    name.
     * 2) The IOs are managed by the unordered_map m_fileData, so we do not
     *    need the ADIOS2 internal management.
     * Since within one m_ADIOS object, the same IO name cannot be used more
     * than once, we ensure different names by using the name counter.
     * This allows to overwrite a file later without error.
     */
    int nameCounter{0};

    /*
     * IO-heavy actions are deferred to a later point. This map stores for
     * each open file (identified by an InvalidatableFile object) an object
     * that manages IO-heavy actions, as well as its ADIOS2 objects, i.e.
     * IO and Engine object.
     * Not to be accessed directly, use getFileData().
     */
    std::unordered_map< InvalidatableFile,
                        std::unique_ptr< detail::BufferedActions >
    > m_fileData;

    std::map< std::string, adios2::Operator > m_operators;

    // Overrides from AbstractIOHandlerImplCommon.

    std::string
        filePositionToString( std::shared_ptr< ADIOS2FilePosition > ) override;

    std::shared_ptr< ADIOS2FilePosition >
    extendFilePosition( std::shared_ptr< ADIOS2FilePosition > const & pos,
                        std::string extend ) override;

    // Helper methods.

    std::unique_ptr< adios2::Operator >
    getCompressionOperator( std::string const & compression );

    /*
     * The name of the ADIOS2 variable associated with this Writable.
     * To be used for Writables that represent a dataset.
     */
    std::string nameOfVariable( Writable * writable );

    /**
     * @brief nameOfAttribute
     * @param writable The Writable at whose level the attribute lies.
     * @param attribute The openPMD name of the attribute.
     * @return The ADIOS2 name of the attribute, consisting of
     * the variable that the attribute is associated with
     * (possibly the empty string, representing no variable)
     * and the actual name.
     */
    std::string nameOfAttribute( Writable * writable, std::string attribute );

    /*
     * Figure out whether the Writable corresponds with a
     * group or a dataset.
     */
    ADIOS2FilePosition::GD groupOrDataset( Writable * );

    detail::BufferedActions & getFileData( InvalidatableFile file );

    void dropFileData( InvalidatableFile file );

    /*
     * Prepare a variable that already exists for an IO
     * operation, including:
     * (1) checking that its datatype matches T.
     * (2) the offset and extent match the variable's shape
     * (3) setting the offset and extent (ADIOS lingo: start
     *     and count)
     */
    template < typename T >
    adios2::Variable< T > verifyDataset( Offset const & offset,
                                         Extent const & extent, adios2::IO & IO,
                                         std::string const & var );
}; // ADIOS2IOHandlerImpl

/*
 * The following strings are used during parsing of the JSON configuration
 * string for the ADIOS2 backend.
 */
namespace ADIOS2Defaults
{
    using const_str = char const * const;
    constexpr const_str str_engine = "engine";
    constexpr const_str str_type = "type";
    constexpr const_str str_params = "parameters";
}

namespace detail
{
    // Helper structs for calls to the switchType function

    struct DatasetReader
    {
        openPMD::ADIOS2IOHandlerImpl * m_impl;


        explicit DatasetReader( openPMD::ADIOS2IOHandlerImpl * impl );


        template < typename T >
        void operator( )( BufferedGet & bp, adios2::IO & IO,
                          adios2::Engine & engine,
                          std::string const & fileName );

        template < int T, typename... Params > void operator( )( Params &&... );
    };

    struct AttributeReader
    {
        template < typename T >
        Datatype operator( )( adios2::IO & IO, std::string name,
                          std::shared_ptr< Attribute::resource > resource );

        template < int n, typename... Params >
        Datatype operator( )( Params &&... );
    };

    struct AttributeWriter
    {
        template < typename T >
        void
        operator( )( ADIOS2IOHandlerImpl * impl, Writable * writable,
                     const Parameter< Operation::WRITE_ATT > & parameters );


        template < int n, typename... Params > void operator( )( Params &&... );
    };

    struct DatasetOpener
    {
        ADIOS2IOHandlerImpl * m_impl;


        explicit DatasetOpener( ADIOS2IOHandlerImpl * impl );


        template < typename T >
        void operator( )( InvalidatableFile, const std::string & varName,
                          Parameter< Operation::OPEN_DATASET > & parameters );


        template < int n, typename... Params > void operator( )( Params &&... );
    };

    struct WriteDataset
    {
        ADIOS2IOHandlerImpl * m_handlerImpl;


        WriteDataset( ADIOS2IOHandlerImpl * handlerImpl );


        template < typename T >
        void operator( )( BufferedPut & bp, adios2::IO & IO,
                          adios2::Engine & engine );

        template < int n, typename... Params > void operator( )( Params &&... );
    };

    struct VariableDefiner
    {
        // Parameters such as DatasetHelper< T >::defineVariable
        template < typename T, typename... Params >
        void operator( )( Params &&... params );

        template< int n, typename... Params >
        void
        operator()( Params &&... );
    };



    // Helper structs to help distinguish valid attribute/variable
    // datatypes from invalid ones


    /*
     * This struct's purpose is to have specialisations
     * for vector and array types, as well as the boolean
     * type (which is not natively supported by ADIOS).
     */
    template < typename T > struct AttributeTypes
    {
        using Attr = adios2::Attribute< T >;
        using BasicType = T;

        static Attr createAttribute( adios2::IO & IO, std::string name,
                                     BasicType value );

        static void
        readAttribute( adios2::IO & IO, std::string name,
                       std::shared_ptr< Attribute::resource > resource );
    };

    template< > struct AttributeTypes< std::complex< long double > >
    {
        using Attr = adios2::Attribute< std::complex< double > >;
        using BasicType = double;

        static Attr createAttribute( adios2::IO &, std::string,
                                     std::complex< long double > )
        {
            throw std::runtime_error(
                "[ADIOS2] Internal error: no support for long double complex attribute types" );
        }

        static void
        readAttribute( adios2::IO &, std::string,
                       std::shared_ptr< Attribute::resource > )
        {
            throw std::runtime_error(
                "[ADIOS2] Internal error: no support for long double complex attribute types" );
        }
    };

    template< > struct AttributeTypes< std::vector< std::complex< long double > > >
    {
        using Attr = adios2::Attribute< std::complex< double > >;
        using BasicType = double;

        static Attr createAttribute( adios2::IO &, std::string,
                                     const std::vector< std::complex< long double > > & )
        {
            throw std::runtime_error(
                "[ADIOS2] Internal error: no support for long double complex vector attribute types" );
        }

        static void
        readAttribute( adios2::IO &, std::string,
                       std::shared_ptr< Attribute::resource > )
        {
            throw std::runtime_error(
                "[ADIOS2] Internal error: no support for long double complex vector attribute types" );
        }
    };

    template < typename T > struct AttributeTypes< std::vector< T > >
    {
        using Attr = adios2::Attribute< T >;
        using BasicType = T;

        static Attr createAttribute( adios2::IO & IO, std::string name,
                                     const std::vector< T > & value );

        static void
        readAttribute( adios2::IO & IO, std::string name,
                       std::shared_ptr< Attribute::resource > resource );
    };

    template < typename T, size_t n >
    struct AttributeTypes< std::array< T, n > >
    {
        using Attr = adios2::Attribute< T >;
        using BasicType = T;

        static Attr createAttribute( adios2::IO & IO, std::string name,
                                     const std::array< T, n > & value );

        static void
        readAttribute( adios2::IO & IO, std::string name,
                       std::shared_ptr< Attribute::resource > resource );
    };

    template <> struct AttributeTypes< bool >
    {
        using rep = detail::bool_representation;
        using Attr = adios2::Attribute< rep >;
        using BasicType = rep;

        static Attr createAttribute( adios2::IO & IO, std::string name,
                                     bool value );

        static void
        readAttribute( adios2::IO & IO, std::string name,
                       std::shared_ptr< Attribute::resource > resource );


        static constexpr rep toRep( bool b )
        {
            return b ? 1U : 0U;
        }


        static constexpr bool fromRep( rep r )
        {
            return r != 0;
        }
    };


    /**
     * This struct's only field indicates whether the template
     * parameter is a valid datatype to use for a dataset
     * (ADIOS2 variable).
     */
    template < typename T > struct DatasetTypes
    {
        static constexpr bool validType = true;
    };

    template < typename T > struct DatasetTypes< std::vector< T > >
    {
        static constexpr bool validType = false;
    };

    template <> struct DatasetTypes< bool >
    {
        static constexpr bool validType = false;
    };

    // missing std::complex< long double > type in ADIOS2 v2.6.0
    template <> struct DatasetTypes< std::complex< long double > >
    {
        static constexpr bool validType = false;
    };

    template < typename T, size_t n > struct DatasetTypes< std::array< T, n > >
    {
        static constexpr bool validType = false;
    };

    /*
     * This struct's purpose is to have exactly two specialisations:
     * (1) for types that are legal to use in a dataset
     * (2) for types that are not legal to use in a dataset
     * The methods in the latter specialisation will fail at runtime.
     */
    template < typename, typename = void > struct DatasetHelper;

    template < typename T >
    struct DatasetHelper<
        T, typename std::enable_if< DatasetTypes< T >::validType >::type >
    {
        openPMD::ADIOS2IOHandlerImpl * m_impl;


        explicit DatasetHelper( openPMD::ADIOS2IOHandlerImpl * impl );


        void openDataset( InvalidatableFile, const std::string & varName,
                          Parameter< Operation::OPEN_DATASET > & parameters );

        void readDataset( BufferedGet &, adios2::IO &, adios2::Engine &,
                          std::string const & fileName );

        /**
         * @brief Define a Variable of type T within the passed IO.
         *
         * @param IO The adios2::IO object within which to define the
         *           variable. The variable can later be retrieved from
         *           the IO using the passed name.
         * @param name As in adios2::IO::DefineVariable
         * @param compressions ADIOS2 operators, including an arbitrary
         *                     number of parameters, to be added to the
         *                     variable upon definition.
         * @param shape As in adios2::IO::DefineVariable
         * @param start As in adios2::IO::DefineVariable
         * @param count As in adios2::IO::DefineVariable
         * @param constantDims As in adios2::IO::DefineVariable
         */
        static void
        defineVariable(
            adios2::IO & IO,
            std::string const & name,
            std::vector< ADIOS2IOHandlerImpl::ParameterizedOperator > const &
                compressions,
            adios2::Dims const & shape = adios2::Dims(),
            adios2::Dims const & start = adios2::Dims(),
            adios2::Dims const & count = adios2::Dims(),
            bool const constantDims = false );

        void writeDataset( BufferedPut &, adios2::IO &, adios2::Engine & );
    };

    template < typename T >
    struct DatasetHelper<
        T, typename std::enable_if< !DatasetTypes< T >::validType >::type >
    {
        explicit DatasetHelper( openPMD::ADIOS2IOHandlerImpl * impl );


        static void throwErr( );

        template < typename... Params > void openDataset( Params &&... );

        template < typename... Params > void readDataset( Params &&... );

        template < typename... Params >
        static void defineVariable( Params &&... );

        template < typename... Params > void writeDataset( Params &&... );
    };

    // Other datatypes used in the ADIOS2IOHandler implementation


    struct BufferedActions;

    /*
     * IO-heavy action to be executed upon flushing.
     */
    struct BufferedAction
    {
        virtual ~BufferedAction( ) = default;

        virtual void run( BufferedActions & ) = 0;
    };

    struct BufferedGet : BufferedAction
    {
        std::string name;
        Parameter< Operation::READ_DATASET > param;

        void run( BufferedActions & ) override;
    };

    struct BufferedPut : BufferedAction
    {
        std::string name;
        Parameter< Operation::WRITE_DATASET > param;

        void run( BufferedActions & ) override;
    };

    struct BufferedAttributeRead : BufferedAction
    {
        Parameter< Operation::READ_ATT > param;
        std::string name;

        void run( BufferedActions & ) override;
    };

    /*
     * Manages per-file information about
     * (1) the file's IO and Engine objects
     * (2) the file's deferred IO-heavy actions
     */
    struct BufferedActions
    {
        BufferedActions( BufferedActions const & ) = delete;

        std::string m_file;
        adios2::IO m_IO;
        std::vector< std::unique_ptr< BufferedAction > > m_buffer;
        /**
         * @brief std::optional would be more idiomatic, but it's not in
         *        the C++11 standard
         * @todo replace with std::optional upon switching to C++17
         */
        std::unique_ptr< adios2::Engine > m_engine;
        adios2::Mode m_mode;
        detail::WriteDataset m_writeDataset;
        detail::DatasetReader m_readDataset;
        detail::AttributeReader m_attributeReader;
        ADIOS2IOHandlerImpl & m_impl;

        using AttributeMap_t = std::map< std::string, adios2::Params >;

        BufferedActions( ADIOS2IOHandlerImpl & impl, InvalidatableFile file );

        ~BufferedActions( );

        void
        configure_IO( ADIOS2IOHandlerImpl & impl );

        adios2::Engine & getEngine( );

        template < typename BA > void enqueue( BA && ba );


        void flush( );

        /*
         * Delete all buffered actions without running them.
         */
        void drop( );

        AttributeMap_t const &
        availableAttributes();

        std::vector< std::string >
        availableAttributesPrefixed( std::string const & prefix );

        /*
         * See description below.
         */
        void
        invalidateAttributesMap();

        AttributeMap_t const &
        availableVariables();

        std::vector< std::string >
        availableVariablesPrefixed( std::string const & prefix );

        /*
         * See description below.
         */
        void
        invalidateVariablesMap();

    private:
        /*
         * ADIOS2 does not give direct access to its internal attribute and
         * variable maps, but will instead give access to copies of them.
         * In order to avoid unnecessary copies, we buffer the returned map.
         * The downside of this is that we need to pay attention to invalidate
         * the map whenever an attribute/variable is altered. In that case, we
         * fetch the map anew.
         * Revisit once https://github.com/openPMD/openPMD-api/issues/563 has
         * been resolved
         * If false, the buffered map has been invalidated and needs to be
         * queried from ADIOS2 again. If true, the buffered map is equivalent to
         * the map that would be returned by a call to
         * IO::Available(Attributes|Variables).
         */
        bool m_availableAttributesValid = false;
        AttributeMap_t m_availableAttributes;

        bool m_availableVariablesValid = false;
        AttributeMap_t m_availableVariables;
    };


} // namespace detail
#endif // openPMD_HAVE_ADIOS2


class ADIOS2IOHandler : public AbstractIOHandler
{
#if openPMD_HAVE_ADIOS2

friend class ADIOS2IOHandlerImpl;

private:
    ADIOS2IOHandlerImpl m_impl;

public:
    ~ADIOS2IOHandler( ) override
    {
        // we must not throw in a destructor
        try
        {
            this->flush( );
        }
        catch( std::exception const & ex )
        {
            std::cerr << "[~ADIOS2IOHandler] An error occurred: " << ex.what() << std::endl;
        }
        catch( ... )
        {
            std::cerr << "[~ADIOS2IOHandler] An error occurred." << std::endl;
        }
    }

#else
public:
#endif

#if openPMD_HAVE_MPI

    ADIOS2IOHandler(
        std::string path,
        Access,
        MPI_Comm,
        nlohmann::json options
    );

#endif

    ADIOS2IOHandler(std::string path, Access, nlohmann::json options );

    std::string backendName() const override { return "ADIOS2"; }

    std::future< void > flush( ) override;
}; // ADIOS2IOHandler
} // namespace openPMD

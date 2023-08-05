// A Bison parser, made by GNU Bison 3.6.3.

// Skeleton implementation for Bison LALR(1) parsers in C++

// Copyright (C) 2002-2015, 2018-2020 Free Software Foundation, Inc.

// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

// As a special exception, you may create a larger work that contains
// part or all of the Bison parser skeleton and distribute that work
// under terms of your choice, so long as that work isn't itself a
// parser generator using the skeleton or a modified version thereof
// as a parser skeleton.  Alternatively, if you modify or redistribute
// the parser skeleton itself, you may (at your option) remove this
// special exception, which will cause the skeleton and the resulting
// Bison output files to be licensed under the GNU General Public
// License without this special exception.

// This special exception was added by the Free Software Foundation in
// version 2.2 of Bison.

// DO NOT RELY ON FEATURES THAT ARE NOT DOCUMENTED in the manual,
// especially those whose name start with YY_ or yy_.  They are
// private implementation details that can be changed or removed.


// Take the name prefix into account.
#define yylex   pytypelex



#include "parser.tab.hh"


// Unqualified %code blocks.
#line 34 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"

namespace {
PyObject* DOT_STRING = PyString_FromString(".");

/* Helper functions for building up lists. */
PyObject* StartList(PyObject* item);
PyObject* AppendList(PyObject* list, PyObject* item);
PyObject* ExtendList(PyObject* dst, PyObject* src);

}  // end namespace


// Check that a python value is not NULL.  This must be a macro because it
// calls YYERROR (which is a goto).
#define CHECK(x, loc) do { if (x == NULL) {\
    ctx->SetErrorLocation(loc); \
    YYERROR; \
  }} while(0)

// pytypelex is generated in lexer.lex.cc, but because it uses semantic_type and
// location, it must be declared here.
int pytypelex(pytype::parser::semantic_type* lvalp, pytype::location* llocp,
              void* scanner);


#line 74 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"


#ifndef YY_
# if defined YYENABLE_NLS && YYENABLE_NLS
#  if ENABLE_NLS
#   include <libintl.h> // FIXME: INFRINGES ON USER NAME SPACE.
#   define YY_(msgid) dgettext ("bison-runtime", msgid)
#  endif
# endif
# ifndef YY_
#  define YY_(msgid) msgid
# endif
#endif


// Whether we are compiled with exception support.
#ifndef YY_EXCEPTIONS
# if defined __GNUC__ && !defined __EXCEPTIONS
#  define YY_EXCEPTIONS 0
# else
#  define YY_EXCEPTIONS 1
# endif
#endif

#define YYRHSLOC(Rhs, K) ((Rhs)[K].location)
/* YYLLOC_DEFAULT -- Set CURRENT to span from RHS[1] to RHS[N].
   If N is 0, then set CURRENT to the empty location which ends
   the previous symbol: RHS[0] (always defined).  */

# ifndef YYLLOC_DEFAULT
#  define YYLLOC_DEFAULT(Current, Rhs, N)                               \
    do                                                                  \
      if (N)                                                            \
        {                                                               \
          (Current).begin  = YYRHSLOC (Rhs, 1).begin;                   \
          (Current).end    = YYRHSLOC (Rhs, N).end;                     \
        }                                                               \
      else                                                              \
        {                                                               \
          (Current).begin = (Current).end = YYRHSLOC (Rhs, 0).end;      \
        }                                                               \
    while (false)
# endif


// Enable debugging if requested.
#if PYTYPEDEBUG

// A pseudo ostream that takes yydebug_ into account.
# define YYCDEBUG if (yydebug_) (*yycdebug_)

# define YY_SYMBOL_PRINT(Title, Symbol)         \
  do {                                          \
    if (yydebug_)                               \
    {                                           \
      *yycdebug_ << Title << ' ';               \
      yy_print_ (*yycdebug_, Symbol);           \
      *yycdebug_ << '\n';                       \
    }                                           \
  } while (false)

# define YY_REDUCE_PRINT(Rule)          \
  do {                                  \
    if (yydebug_)                       \
      yy_reduce_print_ (Rule);          \
  } while (false)

# define YY_STACK_PRINT()               \
  do {                                  \
    if (yydebug_)                       \
      yy_stack_print_ ();                \
  } while (false)

#else // !PYTYPEDEBUG

# define YYCDEBUG if (false) std::cerr
# define YY_SYMBOL_PRINT(Title, Symbol)  YYUSE (Symbol)
# define YY_REDUCE_PRINT(Rule)           static_cast<void> (0)
# define YY_STACK_PRINT()                static_cast<void> (0)

#endif // !PYTYPEDEBUG

#define yyerrok         (yyerrstatus_ = 0)
#define yyclearin       (yyla.clear ())

#define YYACCEPT        goto yyacceptlab
#define YYABORT         goto yyabortlab
#define YYERROR         goto yyerrorlab
#define YYRECOVERING()  (!!yyerrstatus_)

#line 17 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
namespace pytype {
#line 167 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"

  /// Build a parser object.
  parser::parser (void* scanner_yyarg, pytype::Context* ctx_yyarg)
#if PYTYPEDEBUG
    : yydebug_ (false),
      yycdebug_ (&std::cerr),
#else
    :
#endif
      scanner (scanner_yyarg),
      ctx (ctx_yyarg)
  {}

  parser::~parser ()
  {}

  parser::syntax_error::~syntax_error () YY_NOEXCEPT YY_NOTHROW
  {}

  /*---------------.
  | symbol kinds.  |
  `---------------*/

  // basic_symbol.
  template <typename Base>
  parser::basic_symbol<Base>::basic_symbol (const basic_symbol& that)
    : Base (that)
    , value (that.value)
    , location (that.location)
  {}


  /// Constructor for valueless symbols.
  template <typename Base>
  parser::basic_symbol<Base>::basic_symbol (typename Base::kind_type t, YY_MOVE_REF (location_type) l)
    : Base (t)
    , value ()
    , location (l)
  {}

  template <typename Base>
  parser::basic_symbol<Base>::basic_symbol (typename Base::kind_type t, YY_RVREF (semantic_type) v, YY_RVREF (location_type) l)
    : Base (t)
    , value (YY_MOVE (v))
    , location (YY_MOVE (l))
  {}

  template <typename Base>
  parser::symbol_kind_type
  parser::basic_symbol<Base>::type_get () const YY_NOEXCEPT
  {
    return this->kind ();
  }

  template <typename Base>
  bool
  parser::basic_symbol<Base>::empty () const YY_NOEXCEPT
  {
    return this->kind () == symbol_kind::S_YYEMPTY;
  }

  template <typename Base>
  void
  parser::basic_symbol<Base>::move (basic_symbol& s)
  {
    super_type::move (s);
    value = YY_MOVE (s.value);
    location = YY_MOVE (s.location);
  }

  // by_kind.
  parser::by_kind::by_kind ()
    : kind_ (symbol_kind::S_YYEMPTY)
  {}

#if 201103L <= YY_CPLUSPLUS
  parser::by_kind::by_kind (by_kind&& that)
    : kind_ (that.kind_)
  {
    that.clear ();
  }
#endif

  parser::by_kind::by_kind (const by_kind& that)
    : kind_ (that.kind_)
  {}

  parser::by_kind::by_kind (token_kind_type t)
    : kind_ (yytranslate_ (t))
  {}

  void
  parser::by_kind::clear ()
  {
    kind_ = symbol_kind::S_YYEMPTY;
  }

  void
  parser::by_kind::move (by_kind& that)
  {
    kind_ = that.kind_;
    that.clear ();
  }

  parser::symbol_kind_type
  parser::by_kind::kind () const YY_NOEXCEPT
  {
    return kind_;
  }

  parser::symbol_kind_type
  parser::by_kind::type_get () const YY_NOEXCEPT
  {
    return this->kind ();
  }


  // by_state.
  parser::by_state::by_state () YY_NOEXCEPT
    : state (empty_state)
  {}

  parser::by_state::by_state (const by_state& that) YY_NOEXCEPT
    : state (that.state)
  {}

  void
  parser::by_state::clear () YY_NOEXCEPT
  {
    state = empty_state;
  }

  void
  parser::by_state::move (by_state& that)
  {
    state = that.state;
    that.clear ();
  }

  parser::by_state::by_state (state_type s) YY_NOEXCEPT
    : state (s)
  {}

  parser::symbol_kind_type
  parser::by_state::kind () const YY_NOEXCEPT
  {
    if (state == empty_state)
      return symbol_kind::S_YYEMPTY;
    else
      return YY_CAST (symbol_kind_type, yystos_[+state]);
  }

  parser::stack_symbol_type::stack_symbol_type ()
  {}

  parser::stack_symbol_type::stack_symbol_type (YY_RVREF (stack_symbol_type) that)
    : super_type (YY_MOVE (that.state), YY_MOVE (that.value), YY_MOVE (that.location))
  {
#if 201103L <= YY_CPLUSPLUS
    // that is emptied.
    that.state = empty_state;
#endif
  }

  parser::stack_symbol_type::stack_symbol_type (state_type s, YY_MOVE_REF (symbol_type) that)
    : super_type (s, YY_MOVE (that.value), YY_MOVE (that.location))
  {
    // that is emptied.
    that.kind_ = symbol_kind::S_YYEMPTY;
  }

#if YY_CPLUSPLUS < 201103L
  parser::stack_symbol_type&
  parser::stack_symbol_type::operator= (const stack_symbol_type& that)
  {
    state = that.state;
    value = that.value;
    location = that.location;
    return *this;
  }

  parser::stack_symbol_type&
  parser::stack_symbol_type::operator= (stack_symbol_type& that)
  {
    state = that.state;
    value = that.value;
    location = that.location;
    // that is emptied.
    that.state = empty_state;
    return *this;
  }
#endif

  template <typename Base>
  void
  parser::yy_destroy_ (const char* yymsg, basic_symbol<Base>& yysym) const
  {
    if (yymsg)
      YY_SYMBOL_PRINT (yymsg, yysym);

    // User destructor.
    switch (yysym.kind ())
    {
      case 3: // NAME
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 374 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 4: // NUMBER
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 380 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 5: // STRING
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 386 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 6: // LEXERROR
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 392 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 51: // start
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 398 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 52: // unit
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 404 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 53: // alldefs
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 410 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 55: // classdef
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 416 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 56: // class_name
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 422 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 57: // parents
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 428 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 58: // parent_list
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 434 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 59: // parent
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 440 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 60: // maybe_class_funcs
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 446 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 61: // class_funcs
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 452 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 62: // funcdefs
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 458 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 63: // if_stmt
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 464 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 64: // if_and_elifs
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 470 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 65: // class_if_stmt
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 476 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 66: // class_if_and_elifs
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 482 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 67: // if_cond
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 488 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 68: // elif_cond
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 494 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 69: // else_cond
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 500 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 70: // condition
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 506 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 71: // version_tuple
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 512 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 72: // condition_op
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.str)); }
#line 518 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 73: // constantdef
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 524 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 74: // importdef
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 530 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 75: // import_items
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 536 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 76: // import_item
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 542 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 77: // import_name
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 548 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 78: // from_list
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 554 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 79: // from_items
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 560 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 80: // from_item
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 566 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 81: // alias_or_constant
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 572 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 82: // maybe_string_list
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 578 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 83: // string_list
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 584 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 84: // typevardef
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 590 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 85: // typevar_args
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 596 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 86: // typevar_kwargs
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 602 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 87: // typevar_kwarg
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 608 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 88: // funcdef
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 614 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 89: // funcname
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 620 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 90: // decorators
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 626 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 91: // decorator
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 632 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 92: // maybe_async
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 638 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 93: // params
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 644 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 94: // param_list
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 650 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 95: // param
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 656 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 96: // param_type
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 662 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 97: // param_default
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 668 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 98: // param_star_name
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 674 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 99: // return
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 680 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 101: // maybe_body
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 686 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 103: // body
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 692 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 104: // body_stmt
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 698 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 105: // type_parameters
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 704 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 106: // type_parameter
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 710 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 107: // maybe_type_list
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 716 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 108: // type_list
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 722 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 109: // type
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 728 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 110: // named_tuple_fields
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 734 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 111: // named_tuple_field_list
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 740 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 112: // named_tuple_field
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 746 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 114: // coll_named_tuple_fields
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 752 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 115: // coll_named_tuple_field_list
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 758 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 116: // coll_named_tuple_field
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 764 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 117: // typed_dict_fields
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 770 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 118: // typed_dict_field_dict
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 776 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 119: // typed_dict_field
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 782 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 120: // maybe_typed_dict_kwarg
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 788 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 121: // type_tuple_elements
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 794 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 122: // type_tuple_literal
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 800 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 123: // dotted_name
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 806 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 124: // getitem_key
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 812 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 125: // maybe_number
#line 102 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { Py_CLEAR((yysym.value.obj)); }
#line 818 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      default:
        break;
    }
  }

#if PYTYPEDEBUG
  template <typename Base>
  void
  parser::yy_print_ (std::ostream& yyo, const basic_symbol<Base>& yysym) const
  {
    std::ostream& yyoutput = yyo;
    YYUSE (yyoutput);
    if (yysym.empty ())
      yyo << "empty symbol";
    else
      {
        symbol_kind_type yykind = yysym.kind ();
        yyo << (yykind < YYNTOKENS ? "token" : "nterm")
            << ' ' << yysym.name () << " ("
            << yysym.location << ": ";
        YYUSE (yykind);
        yyo << ')';
      }
  }
#endif

  void
  parser::yypush_ (const char* m, YY_MOVE_REF (stack_symbol_type) sym)
  {
    if (m)
      YY_SYMBOL_PRINT (m, sym);
    yystack_.push (YY_MOVE (sym));
  }

  void
  parser::yypush_ (const char* m, state_type s, YY_MOVE_REF (symbol_type) sym)
  {
#if 201103L <= YY_CPLUSPLUS
    yypush_ (m, stack_symbol_type (s, std::move (sym)));
#else
    stack_symbol_type ss (s, sym);
    yypush_ (m, ss);
#endif
  }

  void
  parser::yypop_ (int n)
  {
    yystack_.pop (n);
  }

#if PYTYPEDEBUG
  std::ostream&
  parser::debug_stream () const
  {
    return *yycdebug_;
  }

  void
  parser::set_debug_stream (std::ostream& o)
  {
    yycdebug_ = &o;
  }


  parser::debug_level_type
  parser::debug_level () const
  {
    return yydebug_;
  }

  void
  parser::set_debug_level (debug_level_type l)
  {
    yydebug_ = l;
  }
#endif // PYTYPEDEBUG

  parser::state_type
  parser::yy_lr_goto_state_ (state_type yystate, int yysym)
  {
    int yyr = yypgoto_[yysym - YYNTOKENS] + yystate;
    if (0 <= yyr && yyr <= yylast_ && yycheck_[yyr] == yystate)
      return yytable_[yyr];
    else
      return yydefgoto_[yysym - YYNTOKENS];
  }

  bool
  parser::yy_pact_value_is_default_ (int yyvalue)
  {
    return yyvalue == yypact_ninf_;
  }

  bool
  parser::yy_table_value_is_error_ (int yyvalue)
  {
    return yyvalue == yytable_ninf_;
  }

  int
  parser::operator() ()
  {
    return parse ();
  }

  int
  parser::parse ()
  {
    int yyn;
    /// Length of the RHS of the rule being reduced.
    int yylen = 0;

    // Error handling.
    int yynerrs_ = 0;
    int yyerrstatus_ = 0;

    /// The lookahead symbol.
    symbol_type yyla;

    /// The locations where the error started and ended.
    stack_symbol_type yyerror_range[3];

    /// The return value of parse ().
    int yyresult;

#if YY_EXCEPTIONS
    try
#endif // YY_EXCEPTIONS
      {
    YYCDEBUG << "Starting parse\n";


    /* Initialize the stack.  The initial state will be set in
       yynewstate, since the latter expects the semantical and the
       location values to have been already stored, initialize these
       stacks with a primary value.  */
    yystack_.clear ();
    yypush_ (YY_NULLPTR, 0, YY_MOVE (yyla));

  /*-----------------------------------------------.
  | yynewstate -- push a new symbol on the stack.  |
  `-----------------------------------------------*/
  yynewstate:
    YYCDEBUG << "Entering state " << int (yystack_[0].state) << '\n';
    YY_STACK_PRINT ();

    // Accept?
    if (yystack_[0].state == yyfinal_)
      YYACCEPT;

    goto yybackup;


  /*-----------.
  | yybackup.  |
  `-----------*/
  yybackup:
    // Try to take a decision without lookahead.
    yyn = yypact_[+yystack_[0].state];
    if (yy_pact_value_is_default_ (yyn))
      goto yydefault;

    // Read a lookahead token.
    if (yyla.empty ())
      {
        YYCDEBUG << "Reading a token\n";
#if YY_EXCEPTIONS
        try
#endif // YY_EXCEPTIONS
          {
            yyla.kind_ = yytranslate_ (yylex (&yyla.value, &yyla.location, scanner));
          }
#if YY_EXCEPTIONS
        catch (const syntax_error& yyexc)
          {
            YYCDEBUG << "Caught exception: " << yyexc.what() << '\n';
            error (yyexc);
            goto yyerrlab1;
          }
#endif // YY_EXCEPTIONS
      }
    YY_SYMBOL_PRINT ("Next token is", yyla);

    if (yyla.kind () == symbol_kind::S_YYerror)
    {
      // The scanner already issued an error message, process directly
      // to error recovery.  But do not keep the error token as
      // lookahead, it is too special and may lead us to an endless
      // loop in error recovery. */
      yyla.kind_ = symbol_kind::S_YYUNDEF;
      goto yyerrlab1;
    }

    /* If the proper action on seeing token YYLA.TYPE is to reduce or
       to detect an error, take that action.  */
    yyn += yyla.kind ();
    if (yyn < 0 || yylast_ < yyn || yycheck_[yyn] != yyla.kind ())
      {
        goto yydefault;
      }

    // Reduce or error.
    yyn = yytable_[yyn];
    if (yyn <= 0)
      {
        if (yy_table_value_is_error_ (yyn))
          goto yyerrlab;
        yyn = -yyn;
        goto yyreduce;
      }

    // Count tokens shifted since error; after three, turn off error status.
    if (yyerrstatus_)
      --yyerrstatus_;

    // Shift the lookahead token.
    yypush_ ("Shifting", state_type (yyn), YY_MOVE (yyla));
    goto yynewstate;


  /*-----------------------------------------------------------.
  | yydefault -- do the default action for the current state.  |
  `-----------------------------------------------------------*/
  yydefault:
    yyn = yydefact_[+yystack_[0].state];
    if (yyn == 0)
      goto yyerrlab;
    goto yyreduce;


  /*-----------------------------.
  | yyreduce -- do a reduction.  |
  `-----------------------------*/
  yyreduce:
    yylen = yyr2_[yyn];
    {
      stack_symbol_type yylhs;
      yylhs.state = yy_lr_goto_state_ (yystack_[yylen].state, yyr1_[yyn]);
      /* If YYLEN is nonzero, implement the default value of the
         action: '$$ = $1'.  Otherwise, use the top of the stack.

         Otherwise, the following line sets YYLHS.VALUE to garbage.
         This behavior is undocumented and Bison users should not rely
         upon it.  */
      if (yylen)
        yylhs.value = yystack_[yylen - 1].value;
      else
        yylhs.value = yystack_[0].value;

      // Default location.
      {
        stack_type::slice range (yystack_, yylen);
        YYLLOC_DEFAULT (yylhs.location, range, yylen);
        yyerror_range[1].location = yylhs.location;
      }

      // Perform the reduction.
      YY_REDUCE_PRINT (yyn);
#if YY_EXCEPTIONS
      try
#endif // YY_EXCEPTIONS
        {
          switch (yyn)
            {
  case 2:
#line 135 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
             { ctx->SetAndDelResult((yystack_[1].value.obj)); (yylhs.value.obj) = NULL; }
#line 1089 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 3:
#line 136 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                          { ctx->SetAndDelResult((yystack_[1].value.obj)); (yylhs.value.obj) = NULL; }
#line 1095 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 4:
#line 140 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1101 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 5:
#line 144 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                        { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1107 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 6:
#line 145 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1113 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 7:
#line 146 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                      { (yylhs.value.obj) = (yystack_[1].value.obj); Py_DECREF((yystack_[0].value.obj)); }
#line 1119 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 8:
#line 147 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                              {
      (yylhs.value.obj) = (yystack_[1].value.obj);
      PyObject* tmp = ctx->Call(kAddAliasOrConstant, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yylhs.location);
      Py_DECREF(tmp);
    }
#line 1130 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 9:
#line 153 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                     { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1136 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 10:
#line 154 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                       { (yylhs.value.obj) = (yystack_[1].value.obj); Py_DECREF((yystack_[0].value.obj)); }
#line 1142 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 11:
#line 155 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    {
      PyObject* tmp = ctx->Call(kIfEnd, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yystack_[0].location);
      (yylhs.value.obj) = ExtendList((yystack_[1].value.obj), tmp);
    }
#line 1152 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 12:
#line 160 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = PyList_New(0); }
#line 1158 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 15:
#line 173 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      (yylhs.value.obj) = ctx->Call(kNewClass, "(NNNN)", (yystack_[6].value.obj), (yystack_[4].value.obj), (yystack_[3].value.obj), (yystack_[0].value.obj));
      // Fix location tracking. See funcdef.
      yylhs.location.begin = yystack_[4].location.begin;
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1169 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 16:
#line 182 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
         {
      // Do not borrow the $1 reference since it is also returned later
      // in $$.  Use O instead of N in the format string.
      PyObject* tmp = ctx->Call(kRegisterClassName, "(O)", (yystack_[0].value.obj));
      CHECK(tmp, yylhs.location);
      Py_DECREF(tmp);
      (yylhs.value.obj) = (yystack_[0].value.obj);
    }
#line 1182 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 17:
#line 193 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                        { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1188 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 18:
#line 194 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
            { (yylhs.value.obj) = PyList_New(0); }
#line 1194 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 19:
#line 195 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                 { (yylhs.value.obj) = PyList_New(0); }
#line 1200 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 20:
#line 199 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                           { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1206 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 21:
#line 200 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
           { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1212 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 22:
#line 204 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
         { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1218 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 23:
#line 205 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                  { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1224 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 24:
#line 206 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
               { (yylhs.value.obj) = PyString_FromString("NamedTuple"); }
#line 1230 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 25:
#line 207 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
              {
      (yylhs.value.obj) = ctx->Call(kNewType, "(N)", PyString_FromString("TypedDict"));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1239 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 26:
#line 214 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                       { (yylhs.value.obj) = PyList_New(0); }
#line 1245 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 27:
#line 215 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                              { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1251 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 28:
#line 216 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                           { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1257 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 29:
#line 220 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                     { (yylhs.value.obj) = PyList_New(0); }
#line 1263 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 30:
#line 221 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1269 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 31:
#line 225 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                         { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1275 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 32:
#line 226 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                               {
      PyObject* tmp = ctx->Call(kNewAliasOrConstant, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yylhs.location);
      (yylhs.value.obj) = AppendList((yystack_[1].value.obj), tmp);
    }
#line 1285 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 33:
#line 231 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                     { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1291 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 34:
#line 232 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                           {
      PyObject* tmp = ctx->Call(kIfEnd, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yystack_[0].location);
      (yylhs.value.obj) = ExtendList((yystack_[1].value.obj), tmp);
    }
#line 1301 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 35:
#line 237 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                      { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1307 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 36:
#line 238 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = PyList_New(0); }
#line 1313 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 37:
#line 243 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                     {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1321 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 38:
#line 246 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1327 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 39:
#line 251 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                      {
      (yylhs.value.obj) = Py_BuildValue("[(NN)]", (yystack_[4].value.obj), (yystack_[1].value.obj));
    }
#line 1335 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 40:
#line 255 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                     {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1343 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 41:
#line 268 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                            {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1351 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 42:
#line 271 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1357 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 43:
#line 276 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                       {
      (yylhs.value.obj) = Py_BuildValue("[(NN)]", (yystack_[4].value.obj), (yystack_[1].value.obj));
    }
#line 1365 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 44:
#line 280 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                            {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1373 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 45:
#line 292 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                 { (yylhs.value.obj) = ctx->Call(kIfBegin, "(N)", (yystack_[0].value.obj)); CHECK((yylhs.value.obj), yylhs.location); }
#line 1379 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 46:
#line 296 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                   { (yylhs.value.obj) = ctx->Call(kIfElif, "(N)", (yystack_[0].value.obj)); CHECK((yylhs.value.obj), yylhs.location); }
#line 1385 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 47:
#line 300 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
         { (yylhs.value.obj) = ctx->Call(kIfElse, "()"); CHECK((yylhs.value.obj), yylhs.location); }
#line 1391 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 48:
#line 304 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                    {
      (yylhs.value.obj) = Py_BuildValue("((NO)sN)", (yystack_[2].value.obj), Py_None, (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1399 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 49:
#line 307 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                           {
      (yylhs.value.obj) = Py_BuildValue("((NO)sN)", (yystack_[2].value.obj), Py_None, (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1407 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 50:
#line 310 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                        {
      (yylhs.value.obj) = Py_BuildValue("((NN)sN)", (yystack_[5].value.obj), (yystack_[3].value.obj), (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1415 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 51:
#line 313 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                               {
      (yylhs.value.obj) = Py_BuildValue("((NN)sN)", (yystack_[5].value.obj), (yystack_[3].value.obj), (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1423 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 52:
#line 316 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                            { (yylhs.value.obj) = Py_BuildValue("(NsN)", (yystack_[2].value.obj), "and", (yystack_[0].value.obj)); }
#line 1429 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 53:
#line 317 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                           { (yylhs.value.obj) = Py_BuildValue("(NsN)", (yystack_[2].value.obj), "or", (yystack_[0].value.obj)); }
#line 1435 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 54:
#line 318 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                      { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1441 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 55:
#line 322 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                       { (yylhs.value.obj) = Py_BuildValue("(N)", (yystack_[2].value.obj)); }
#line 1447 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 56:
#line 323 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                              { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj)); }
#line 1453 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 57:
#line 324 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                         {
      (yylhs.value.obj) = Py_BuildValue("(NNN)", (yystack_[5].value.obj), (yystack_[3].value.obj), (yystack_[1].value.obj));
    }
#line 1461 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 58:
#line 330 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { (yylhs.value.str) = "<"; }
#line 1467 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 59:
#line 331 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { (yylhs.value.str) = ">"; }
#line 1473 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 60:
#line 332 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { (yylhs.value.str) = "<="; }
#line 1479 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 61:
#line 333 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { (yylhs.value.str) = ">="; }
#line 1485 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 62:
#line 334 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { (yylhs.value.str) = "=="; }
#line 1491 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 63:
#line 335 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { (yylhs.value.str) = "!="; }
#line 1497 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 64:
#line 339 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1506 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 65:
#line 343 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1515 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 66:
#line 347 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1524 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 67:
#line 351 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                      {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), ctx->Value(kAnything));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1533 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 68:
#line 355 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                         {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[5].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1542 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 69:
#line 359 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1551 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 70:
#line 363 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                 {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[5].value.obj), (yystack_[3].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1560 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 71:
#line 367 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                         {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", PyString_FromString("TypedDict"), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1569 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 72:
#line 371 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                      {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", PyString_FromString("TypedDict"), (yystack_[3].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1578 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 73:
#line 378 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                          {
      (yylhs.value.obj) = ctx->Call(kAddImport, "(ON)", Py_None, (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1587 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 74:
#line 382 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                        {
      (yylhs.value.obj) = ctx->Call(kAddImport, "(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1596 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 75:
#line 386 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                {
      // Special-case "from . import" and pass in a __PACKAGE__ token that
      // the Python parser code will rewrite to the current package name.
      (yylhs.value.obj) = ctx->Call(kAddImport, "(sN)", "__PACKAGE__", (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1607 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 76:
#line 392 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                    {
      // Special-case "from .. import" and pass in a __PARENT__ token that
      // the Python parser code will rewrite to the parent package name.
      (yylhs.value.obj) = ctx->Call(kAddImport, "(sN)", "__PARENT__", (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1618 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 77:
#line 401 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                 { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1624 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 78:
#line 402 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1630 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 79:
#line 406 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1636 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 80:
#line 407 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                        { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1642 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 81:
#line 412 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1648 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 82:
#line 413 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    {
      (yylhs.value.obj) = PyString_FromFormat(".%s", PyString_AsString((yystack_[0].value.obj)));
      Py_DECREF((yystack_[0].value.obj));
    }
#line 1657 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 83:
#line 420 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1663 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 84:
#line 421 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                       { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1669 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 85:
#line 422 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                           { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 1675 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 86:
#line 426 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                             { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1681 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 87:
#line 427 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
              { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1687 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 88:
#line 431 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1693 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 89:
#line 432 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
               {
      (yylhs.value.obj) = PyString_FromString("NamedTuple");
    }
#line 1701 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 90:
#line 435 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    {
      (yylhs.value.obj) = PyString_FromString("namedtuple");
    }
#line 1709 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 91:
#line 438 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
              {
      (yylhs.value.obj) = PyString_FromString("TypedDict");
    }
#line 1717 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 92:
#line 441 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
            {
      (yylhs.value.obj) = PyString_FromString("TypeVar");
    }
#line 1725 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 93:
#line 444 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        {
      (yylhs.value.obj) = PyString_FromString("*");
    }
#line 1733 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 94:
#line 447 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                 { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1739 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 95:
#line 451 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj)); }
#line 1745 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 96:
#line 452 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                         { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[5].value.obj), (yystack_[2].value.obj)); }
#line 1751 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 97:
#line 456 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                            { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1757 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 98:
#line 457 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = PyList_New(0); }
#line 1763 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 99:
#line 461 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                           { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1769 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 100:
#line 462 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
           { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1775 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 101:
#line 466 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                 {
      (yylhs.value.obj) = ctx->Call(kAddTypeVar, "(NNN)", (yystack_[6].value.obj), (yystack_[2].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1784 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 102:
#line 473 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = Py_BuildValue("(OO)", Py_None, Py_None); }
#line 1790 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 103:
#line 474 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                  { (yylhs.value.obj) = Py_BuildValue("(NO)", (yystack_[0].value.obj), Py_None); }
#line 1796 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 104:
#line 475 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                       { (yylhs.value.obj) = Py_BuildValue("(ON)", Py_None, (yystack_[0].value.obj)); }
#line 1802 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 105:
#line 476 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                     { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1808 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 106:
#line 480 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                     { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1814 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 107:
#line 481 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                  { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1820 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 108:
#line 485 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                  { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1826 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 109:
#line 487 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1832 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 110:
#line 492 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
               {
      (yylhs.value.obj) = ctx->Call(kNewFunction, "(NONNNN)", (yystack_[9].value.obj), (yystack_[8].value.obj), (yystack_[6].value.obj), (yystack_[3].value.obj), (yystack_[1].value.obj), (yystack_[0].value.obj));
      // Decorators is nullable and messes up the location tracking by
      // using the previous symbol as the start location for this production,
      // which is very misleading.  It is better to ignore decorators and
      // pretend the production started with DEF.  Even when decorators are
      // present the error line will be close enough to be helpful.
      yylhs.location.begin = yystack_[7].location.begin;
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1847 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 111:
#line 505 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
         { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1853 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 112:
#line 506 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { (yylhs.value.obj) = PyString_FromString("namedtuple"); }
#line 1859 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 113:
#line 507 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
              { (yylhs.value.obj) = PyString_FromString("TypedDict"); }
#line 1865 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 114:
#line 511 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                         { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1871 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 115:
#line 512 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = PyList_New(0); }
#line 1877 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 116:
#line 516 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                      { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1883 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 117:
#line 520 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
          { (yylhs.value.obj) = Py_True; }
#line 1889 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 118:
#line 521 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = Py_False; }
#line 1895 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 119:
#line 525 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                           { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1901 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 120:
#line 526 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = PyList_New(0); }
#line 1907 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 121:
#line 538 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                           { (yylhs.value.obj) = AppendList((yystack_[3].value.obj), (yystack_[0].value.obj)); }
#line 1913 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 122:
#line 539 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
          { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1919 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 123:
#line 543 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                  { (yylhs.value.obj) = Py_BuildValue("(NNN)", (yystack_[2].value.obj), (yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1925 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 124:
#line 544 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { (yylhs.value.obj) = Py_BuildValue("(sOO)", "*", Py_None, Py_None); }
#line 1931 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 125:
#line 545 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                               { (yylhs.value.obj) = Py_BuildValue("(NNO)", (yystack_[1].value.obj), (yystack_[0].value.obj), Py_None); }
#line 1937 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 126:
#line 546 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
             { (yylhs.value.obj) = ctx->Value(kEllipsis); }
#line 1943 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 127:
#line 550 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
             { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1949 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 128:
#line 551 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { Py_INCREF(Py_None); (yylhs.value.obj) = Py_None; }
#line 1955 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 129:
#line 555 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
             { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1961 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 130:
#line 556 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
               { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1967 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 131:
#line 557 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                 { (yylhs.value.obj) = ctx->Value(kEllipsis); }
#line 1973 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 132:
#line 558 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { Py_INCREF(Py_None); (yylhs.value.obj) = Py_None; }
#line 1979 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 133:
#line 562 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
             { (yylhs.value.obj) = PyString_FromFormat("*%s", PyString_AsString((yystack_[0].value.obj))); }
#line 1985 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 134:
#line 563 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                 { (yylhs.value.obj) = PyString_FromFormat("**%s", PyString_AsString((yystack_[0].value.obj))); }
#line 1991 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 135:
#line 567 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
               { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1997 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 136:
#line 568 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = ctx->Value(kAnything); }
#line 2003 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 137:
#line 572 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                     { Py_DecRef((yystack_[0].value.obj)); }
#line 2009 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 138:
#line 576 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                      { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 2015 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 139:
#line 577 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                           { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 2021 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 140:
#line 578 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
               { (yylhs.value.obj) = PyList_New(0); }
#line 2027 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 148:
#line 592 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                   { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 2033 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 149:
#line 593 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
              { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 2039 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 150:
#line 597 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                  { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2045 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 151:
#line 598 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
               { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2051 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 152:
#line 599 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                       { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 2057 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 153:
#line 603 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                       { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2063 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 154:
#line 604 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                   { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 2069 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 155:
#line 608 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
         { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2075 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 156:
#line 609 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
             { (yylhs.value.obj) = ctx->Value(kEllipsis); }
#line 2081 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 157:
#line 611 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
           { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2087 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 158:
#line 612 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
           { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2093 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 159:
#line 614 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                            {
      (yylhs.value.obj) = ctx->Call(kNewType, "(sN)", "tuple", (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2102 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 160:
#line 621 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                          { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 2108 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 161:
#line 622 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = PyList_New(0); }
#line 2114 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 162:
#line 626 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                       { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2120 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 163:
#line 627 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
         { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 2126 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 164:
#line 631 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                {
      (yylhs.value.obj) = ctx->Call(kNewType, "(N)", (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2135 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 165:
#line 635 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                {
      (yylhs.value.obj) = ctx->Call(kNewType, "(NN)", (yystack_[4].value.obj), PyList_New(0));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2144 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 166:
#line 639 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                    {
      (yylhs.value.obj) = ctx->Call(kNewType, "(NN)", (yystack_[4].value.obj), (yystack_[2].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2153 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 167:
#line 643 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                                 {
      (yylhs.value.obj) = ctx->Call(kNewNamedTuple, "(NN)", (yystack_[4].value.obj), (yystack_[2].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2162 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 168:
#line 647 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                                           {
      (yylhs.value.obj) = ctx->Call(kNewNamedTuple, "(NN)", (yystack_[4].value.obj), (yystack_[2].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2171 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 169:
#line 651 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                                          {
      (yylhs.value.obj) = ctx->Call(kNewTypedDict, "(NNN)", (yystack_[4].value.obj), (yystack_[2].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2180 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 170:
#line 655 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                 { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 2186 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 171:
#line 656 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                  { (yylhs.value.obj) = ctx->Call(kNewIntersectionType, "([NN])", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2192 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 172:
#line 657 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                 { (yylhs.value.obj) = ctx->Call(kNewUnionType, "([NN])", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2198 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 173:
#line 658 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { (yylhs.value.obj) = ctx->Value(kAnything); }
#line 2204 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 174:
#line 659 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
            { (yylhs.value.obj) = ctx->Value(kNothing); }
#line 2210 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 175:
#line 663 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                               { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 2216 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 176:
#line 664 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
            { (yylhs.value.obj) = PyList_New(0); }
#line 2222 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 177:
#line 668 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                 { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2228 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 178:
#line 669 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                      { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 2234 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 179:
#line 673 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                         { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[2].value.obj)); }
#line 2240 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 182:
#line 682 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                    { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 2246 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 183:
#line 683 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
            { (yylhs.value.obj) = PyList_New(0); }
#line 2252 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 184:
#line 687 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                           {
      (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj));
    }
#line 2260 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 185:
#line 690 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                           { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 2266 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 186:
#line 694 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
           { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[0].value.obj), ctx->Value(kAnything)); }
#line 2272 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 187:
#line 698 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                              { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 2278 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 188:
#line 699 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
            { (yylhs.value.obj) = PyDict_New(); }
#line 2284 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 189:
#line 703 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                               {
      PyDict_Update((yystack_[2].value.obj), (yystack_[0].value.obj));
      (yylhs.value.obj) = (yystack_[2].value.obj);
      Py_DECREF((yystack_[0].value.obj));
    }
#line 2294 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 190:
#line 708 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                     { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2300 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 191:
#line 712 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                    { (yylhs.value.obj) = Py_BuildValue("{N: N}", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2306 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 192:
#line 716 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                  { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj)); }
#line 2312 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 193:
#line 717 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = Py_None; }
#line 2318 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 194:
#line 724 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                 { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2324 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 195:
#line 725 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                  { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2330 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 196:
#line 734 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                            {
      Py_DECREF((yystack_[2].value.obj));
      (yylhs.value.obj) = ctx->Value(kTuple);
    }
#line 2339 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 197:
#line 739 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                     {
      Py_DECREF((yystack_[2].value.obj));
      (yylhs.value.obj) = ctx->Value(kTuple);
    }
#line 2348 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 198:
#line 745 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
             {
      Py_DECREF((yystack_[1].value.obj));
      (yylhs.value.obj) = ctx->Value(kTuple);
    }
#line 2357 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 199:
#line 752 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
         { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2363 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 200:
#line 753 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                         {
#if PY_MAJOR_VERSION >= 3
      (yystack_[2].value.obj) = PyUnicode_Concat((yystack_[2].value.obj), DOT_STRING);
      (yystack_[2].value.obj) = PyUnicode_Concat((yystack_[2].value.obj), (yystack_[0].value.obj));
      Py_DECREF((yystack_[0].value.obj));
#else
      PyString_Concat(&(yystack_[2].value.obj), DOT_STRING);
      PyString_ConcatAndDel(&(yystack_[2].value.obj), (yystack_[0].value.obj));
#endif
      (yylhs.value.obj) = (yystack_[2].value.obj);
    }
#line 2379 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 201:
#line 767 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
           { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2385 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 202:
#line 768 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                  {
      PyObject* slice = PySlice_New((yystack_[2].value.obj), (yystack_[0].value.obj), NULL);
      CHECK(slice, yylhs.location);
      (yylhs.value.obj) = slice;
    }
#line 2395 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 203:
#line 773 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                                                   {
      PyObject* slice = PySlice_New((yystack_[4].value.obj), (yystack_[2].value.obj), (yystack_[0].value.obj));
      CHECK(slice, yylhs.location);
      (yylhs.value.obj) = slice;
    }
#line 2405 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 204:
#line 781 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
           { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2411 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 205:
#line 782 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
                { (yylhs.value.obj) = NULL; }
#line 2417 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;


#line 2421 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"

            default:
              break;
            }
        }
#if YY_EXCEPTIONS
      catch (const syntax_error& yyexc)
        {
          YYCDEBUG << "Caught exception: " << yyexc.what() << '\n';
          error (yyexc);
          YYERROR;
        }
#endif // YY_EXCEPTIONS
      YY_SYMBOL_PRINT ("-> $$ =", yylhs);
      yypop_ (yylen);
      yylen = 0;

      // Shift the result of the reduction.
      yypush_ (YY_NULLPTR, YY_MOVE (yylhs));
    }
    goto yynewstate;


  /*--------------------------------------.
  | yyerrlab -- here on detecting error.  |
  `--------------------------------------*/
  yyerrlab:
    // If not already recovering from an error, report this error.
    if (!yyerrstatus_)
      {
        ++yynerrs_;
        context yyctx (*this, yyla);
        std::string msg = yysyntax_error_ (yyctx);
        error (yyla.location, YY_MOVE (msg));
      }


    yyerror_range[1].location = yyla.location;
    if (yyerrstatus_ == 3)
      {
        /* If just tried and failed to reuse lookahead token after an
           error, discard it.  */

        // Return failure if at end of input.
        if (yyla.kind () == symbol_kind::S_YYEOF)
          YYABORT;
        else if (!yyla.empty ())
          {
            yy_destroy_ ("Error: discarding", yyla);
            yyla.clear ();
          }
      }

    // Else will try to reuse lookahead token after shifting the error token.
    goto yyerrlab1;


  /*---------------------------------------------------.
  | yyerrorlab -- error raised explicitly by YYERROR.  |
  `---------------------------------------------------*/
  yyerrorlab:
    /* Pacify compilers when the user code never invokes YYERROR and
       the label yyerrorlab therefore never appears in user code.  */
    if (false)
      YYERROR;

    /* Do not reclaim the symbols of the rule whose action triggered
       this YYERROR.  */
    yypop_ (yylen);
    yylen = 0;
    YY_STACK_PRINT ();
    goto yyerrlab1;


  /*-------------------------------------------------------------.
  | yyerrlab1 -- common code for both syntax error and YYERROR.  |
  `-------------------------------------------------------------*/
  yyerrlab1:
    yyerrstatus_ = 3;   // Each real token shifted decrements this.
    // Pop stack until we find a state that shifts the error token.
    for (;;)
      {
        yyn = yypact_[+yystack_[0].state];
        if (!yy_pact_value_is_default_ (yyn))
          {
            yyn += symbol_kind::S_YYerror;
            if (0 <= yyn && yyn <= yylast_
                && yycheck_[yyn] == symbol_kind::S_YYerror)
              {
                yyn = yytable_[yyn];
                if (0 < yyn)
                  break;
              }
          }

        // Pop the current state because it cannot handle the error token.
        if (yystack_.size () == 1)
          YYABORT;

        yyerror_range[1].location = yystack_[0].location;
        yy_destroy_ ("Error: popping", yystack_[0]);
        yypop_ ();
        YY_STACK_PRINT ();
      }
    {
      stack_symbol_type error_token;

      yyerror_range[2].location = yyla.location;
      YYLLOC_DEFAULT (error_token.location, yyerror_range, 2);

      // Shift the error token.
      error_token.state = state_type (yyn);
      yypush_ ("Shifting", YY_MOVE (error_token));
    }
    goto yynewstate;


  /*-------------------------------------.
  | yyacceptlab -- YYACCEPT comes here.  |
  `-------------------------------------*/
  yyacceptlab:
    yyresult = 0;
    goto yyreturn;


  /*-----------------------------------.
  | yyabortlab -- YYABORT comes here.  |
  `-----------------------------------*/
  yyabortlab:
    yyresult = 1;
    goto yyreturn;


  /*-----------------------------------------------------.
  | yyreturn -- parsing is finished, return the result.  |
  `-----------------------------------------------------*/
  yyreturn:
    if (!yyla.empty ())
      yy_destroy_ ("Cleanup: discarding lookahead", yyla);

    /* Do not reclaim the symbols of the rule whose action triggered
       this YYABORT or YYACCEPT.  */
    yypop_ (yylen);
    YY_STACK_PRINT ();
    while (1 < yystack_.size ())
      {
        yy_destroy_ ("Cleanup: popping", yystack_[0]);
        yypop_ ();
      }

    return yyresult;
  }
#if YY_EXCEPTIONS
    catch (...)
      {
        YYCDEBUG << "Exception caught: cleaning lookahead and stack\n";
        // Do not try to display the values of the reclaimed symbols,
        // as their printers might throw an exception.
        if (!yyla.empty ())
          yy_destroy_ (YY_NULLPTR, yyla);

        while (1 < yystack_.size ())
          {
            yy_destroy_ (YY_NULLPTR, yystack_[0]);
            yypop_ ();
          }
        throw;
      }
#endif // YY_EXCEPTIONS
  }

  void
  parser::error (const syntax_error& yyexc)
  {
    error (yyexc.location, yyexc.what ());
  }

  /* Return YYSTR after stripping away unnecessary quotes and
     backslashes, so that it's suitable for yyerror.  The heuristic is
     that double-quoting is unnecessary unless the string contains an
     apostrophe, a comma, or backslash (other than backslash-backslash).
     YYSTR is taken from yytname.  */
  std::string
  parser::yytnamerr_ (const char *yystr)
  {
    if (*yystr == '"')
      {
        std::string yyr;
        char const *yyp = yystr;

        for (;;)
          switch (*++yyp)
            {
            case '\'':
            case ',':
              goto do_not_strip_quotes;

            case '\\':
              if (*++yyp != '\\')
                goto do_not_strip_quotes;
              else
                goto append;

            append:
            default:
              yyr += *yyp;
              break;

            case '"':
              return yyr;
            }
      do_not_strip_quotes: ;
      }

    return yystr;
  }

  std::string
  parser::symbol_name (symbol_kind_type yysymbol)
  {
    return yytnamerr_ (yytname_[yysymbol]);
  }



  // parser::context.
  parser::context::context (const parser& yyparser, const symbol_type& yyla)
    : yyparser_ (yyparser)
    , yyla_ (yyla)
  {}

  int
  parser::context::expected_tokens (symbol_kind_type yyarg[], int yyargn) const
  {
    // Actual number of expected tokens
    int yycount = 0;

    int yyn = yypact_[+yyparser_.yystack_[0].state];
    if (!yy_pact_value_is_default_ (yyn))
      {
        /* Start YYX at -YYN if negative to avoid negative indexes in
           YYCHECK.  In other words, skip the first -YYN actions for
           this state because they are default actions.  */
        int yyxbegin = yyn < 0 ? -yyn : 0;
        // Stay within bounds of both yycheck and yytname.
        int yychecklim = yylast_ - yyn + 1;
        int yyxend = yychecklim < YYNTOKENS ? yychecklim : YYNTOKENS;
        for (int yyx = yyxbegin; yyx < yyxend; ++yyx)
          if (yycheck_[yyx + yyn] == yyx && yyx != symbol_kind::S_YYerror
              && !yy_table_value_is_error_ (yytable_[yyx + yyn]))
            {
              if (!yyarg)
                ++yycount;
              else if (yycount == yyargn)
                return 0;
              else
                yyarg[yycount++] = YY_CAST (symbol_kind_type, yyx);
            }
      }

    if (yyarg && yycount == 0 && 0 < yyargn)
      yyarg[0] = symbol_kind::S_YYEMPTY;
    return yycount;
  }



  int
  parser::yy_syntax_error_arguments_ (const context& yyctx,
                                                 symbol_kind_type yyarg[], int yyargn) const
  {
    /* There are many possibilities here to consider:
       - If this state is a consistent state with a default action, then
         the only way this function was invoked is if the default action
         is an error action.  In that case, don't check for expected
         tokens because there are none.
       - The only way there can be no lookahead present (in yyla) is
         if this state is a consistent state with a default action.
         Thus, detecting the absence of a lookahead is sufficient to
         determine that there is no unexpected or expected token to
         report.  In that case, just report a simple "syntax error".
       - Don't assume there isn't a lookahead just because this state is
         a consistent state with a default action.  There might have
         been a previous inconsistent state, consistent state with a
         non-default action, or user semantic action that manipulated
         yyla.  (However, yyla is currently not documented for users.)
       - Of course, the expected token list depends on states to have
         correct lookahead information, and it depends on the parser not
         to perform extra reductions after fetching a lookahead from the
         scanner and before detecting a syntax error.  Thus, state merging
         (from LALR or IELR) and default reductions corrupt the expected
         token list.  However, the list is correct for canonical LR with
         one exception: it will still contain any token that will not be
         accepted due to an error action in a later state.
    */

    if (!yyctx.lookahead ().empty ())
      {
        if (yyarg)
          yyarg[0] = yyctx.token ();
        int yyn = yyctx.expected_tokens (yyarg ? yyarg + 1 : yyarg, yyargn - 1);
        return yyn + 1;
      }
    return 0;
  }

  // Generate an error message.
  std::string
  parser::yysyntax_error_ (const context& yyctx) const
  {
    // Its maximum.
    enum { YYARGS_MAX = 5 };
    // Arguments of yyformat.
    symbol_kind_type yyarg[YYARGS_MAX];
    int yycount = yy_syntax_error_arguments_ (yyctx, yyarg, YYARGS_MAX);

    char const* yyformat = YY_NULLPTR;
    switch (yycount)
      {
#define YYCASE_(N, S)                         \
        case N:                               \
          yyformat = S;                       \
        break
      default: // Avoid compiler warnings.
        YYCASE_ (0, YY_("syntax error"));
        YYCASE_ (1, YY_("syntax error, unexpected %s"));
        YYCASE_ (2, YY_("syntax error, unexpected %s, expecting %s"));
        YYCASE_ (3, YY_("syntax error, unexpected %s, expecting %s or %s"));
        YYCASE_ (4, YY_("syntax error, unexpected %s, expecting %s or %s or %s"));
        YYCASE_ (5, YY_("syntax error, unexpected %s, expecting %s or %s or %s or %s"));
#undef YYCASE_
      }

    std::string yyres;
    // Argument number.
    std::ptrdiff_t yyi = 0;
    for (char const* yyp = yyformat; *yyp; ++yyp)
      if (yyp[0] == '%' && yyp[1] == 's' && yyi < yycount)
        {
          yyres += symbol_name (yyarg[yyi++]);
          ++yyp;
        }
      else
        yyres += *yyp;
    return yyres;
  }


  const short parser::yypact_ninf_ = -299;

  const short parser::yytable_ninf_ = -205;

  const short
  parser::yypact_[] =
  {
     -12,  -299,    38,    85,   394,    94,  -299,  -299,   167,    28,
     103,    19,    97,  -299,  -299,   166,   116,  -299,  -299,  -299,
    -299,  -299,    34,  -299,   268,    25,  -299,    28,   347,   392,
     249,  -299,    -4,     8,   145,   151,   268,  -299,    28,   169,
     193,   191,  -299,   227,   103,  -299,   232,  -299,   222,   233,
     250,   268,  -299,   271,   302,  -299,  -299,   266,   277,   268,
     339,   369,  -299,   142,    28,    28,  -299,  -299,  -299,  -299,
     345,  -299,  -299,   355,    32,   382,   103,  -299,  -299,   389,
     314,    16,  -299,   314,   365,   347,   341,   359,  -299,  -299,
     362,   114,   171,   408,   421,   426,   375,   268,   268,   379,
    -299,   149,   428,   268,   237,   401,  -299,   396,   402,  -299,
    -299,  -299,   424,  -299,   406,   403,   410,  -299,  -299,   442,
    -299,  -299,  -299,  -299,   429,  -299,  -299,  -299,  -299,   276,
    -299,   414,   411,  -299,   314,    22,   414,   425,  -299,  -299,
    -299,   331,   216,   415,  -299,  -299,  -299,  -299,   416,   417,
     418,   419,  -299,   439,  -299,   414,  -299,  -299,  -299,   223,
     268,   420,  -299,   387,   422,   152,   245,   268,   427,   414,
     449,  -299,   400,   455,   423,   459,   371,  -299,   276,   414,
    -299,   414,   354,   364,  -299,   430,   222,   250,  -299,   378,
    -299,   387,   414,   414,   431,   432,   433,  -299,   434,   435,
     436,   387,   187,   437,   305,   440,  -299,  -299,   387,   387,
    -299,  -299,  -299,    86,  -299,   438,    55,  -299,  -299,   160,
    -299,  -299,  -299,  -299,  -299,   268,  -299,   309,   288,    31,
     265,   441,    64,   441,     4,   444,  -299,  -299,   268,  -299,
    -299,  -299,   445,   447,  -299,   448,  -299,  -299,  -299,   455,
     386,  -299,  -299,   387,  -299,  -299,  -299,   307,  -299,   414,
     452,  -299,    17,   443,   450,  -299,   452,   458,  -299,   451,
    -299,  -299,   446,  -299,  -299,   453,  -299,   456,   457,  -299,
     460,  -299,   462,  -299,   463,   387,   273,   464,   305,  -299,
    -299,   466,    93,   465,   117,  -299,  -299,   268,   467,  -299,
     487,   469,   130,  -299,  -299,   461,   468,   454,  -299,   491,
     470,  -299,   498,   497,   471,   473,  -299,  -299,   387,   445,
    -299,   447,   472,   475,  -299,   356,  -299,  -299,   166,   478,
    -299,  -299,  -299,   387,   221,  -299,  -299,   268,   479,    31,
     268,  -299,  -299,  -299,  -299,  -299,  -299,  -299,   268,  -299,
    -299,   195,   480,   481,   474,  -299,  -299,  -299,   387,   246,
    -299,  -299,  -299,   174,   174,   477,   486,  -299,   336,   292,
     414,   482,  -299,  -299,  -299,   127,   483,   268,   489,    95,
    -299,   492,   399,  -299,  -299,  -299,   217,   361,  -299,   268,
     219,  -299,  -299,  -299,  -299,   106,   493,  -299,  -299,   387,
     490,  -299,  -299,  -299
  };

  const unsigned char
  parser::yydefact_[] =
  {
      12,    12,     0,     0,   115,     0,     1,     2,     0,     0,
       0,     0,     0,     9,    11,    38,     0,     5,     7,     8,
      10,     6,   118,     3,     0,     0,   199,     0,    45,     0,
      14,    78,    79,     0,     0,    81,     0,    47,     0,     0,
       0,     0,   117,     0,     0,   114,     0,   174,     0,     0,
       0,     0,   173,    14,   164,    64,    65,     0,    67,     0,
      98,    14,    66,     0,     0,     0,    62,    63,    60,    61,
     205,    58,    59,     0,     0,     0,     0,    73,    13,     0,
       0,     0,    82,     0,    14,    46,     0,     0,    12,    16,
      19,    14,     0,     0,     0,     0,     0,     0,     0,     0,
      69,     0,     0,     0,     0,   181,   100,     0,   181,   198,
      95,    54,    53,    52,   201,     0,     0,   200,    48,     0,
      49,   137,    77,    80,    88,    89,    90,    91,    92,     0,
      93,    14,    83,    87,     0,     0,    14,     0,    71,    12,
      12,   115,     0,     0,   116,   111,   112,   113,     0,     0,
       0,     0,   170,   172,   171,    14,   157,   158,   156,     0,
     161,   181,   154,   155,   102,    14,     0,   180,     0,    14,
     180,    97,     0,   205,     0,     0,     0,    75,     0,    14,
      74,    14,   115,   115,    39,   199,    24,    25,    18,     0,
      21,    22,    14,    14,     0,     0,     0,    70,     0,     0,
     181,   163,   180,     0,     0,     0,    68,   197,   195,   194,
     196,    96,    99,     0,   204,   202,     0,    94,    84,     0,
      86,    76,    72,    40,    37,     0,    17,     0,     0,   120,
       0,   181,     0,   181,     0,   181,   165,   159,   180,   160,
     153,   166,   199,   104,   107,   103,   101,    50,    51,   205,
       0,    55,    85,    23,    20,   206,   207,    36,    15,    14,
     128,   126,   124,     0,   181,   122,   128,     0,   176,   181,
     178,   180,     0,   186,   183,   181,   185,     0,     0,   188,
     181,   190,   180,   193,     0,   162,     0,     0,     0,   203,
      56,     0,    36,     0,   115,    29,    26,     0,   132,   133,
       0,   136,    14,   119,   125,     0,   180,     0,   167,   180,
       0,   168,     0,   180,     0,     0,   169,   109,   108,     0,
     106,   105,     0,     0,    27,     0,    35,    34,    42,     0,
      31,    32,    33,   127,     0,   123,   134,     0,   147,     0,
       0,   177,   175,   184,   182,   191,   189,   187,     0,    57,
      28,     0,     0,     0,     0,   129,   130,   131,   135,     0,
     110,   140,   121,   181,   181,     0,     0,    36,     0,     0,
     141,     0,   192,    36,    36,   115,     0,     0,     0,     0,
     149,     0,     0,   143,   142,   179,   115,   115,    43,     0,
     151,   146,   139,   148,   145,     0,     0,    44,    41,   150,
       0,   138,   144,   152
  };

  const short
  parser::yypgoto_[] =
  {
    -299,  -299,   502,   -84,   -48,  -291,  -299,  -299,  -299,   239,
    -299,   176,     1,  -299,  -299,  -299,  -299,  -286,   182,   190,
      48,   310,   357,  -284,  -299,  -299,   476,   515,   -76,   404,
    -152,  -276,  -299,  -299,  -299,  -299,   240,   243,  -271,  -299,
    -299,  -299,  -299,  -299,  -299,   192,   269,  -299,  -299,  -299,
    -236,  -299,  -299,   150,  -298,  -299,   332,  -299,   333,   -24,
    -299,  -299,   230,  -107,  -299,  -299,   229,  -299,  -299,   226,
    -299,  -299,  -299,     6,  -299,  -171,  -222
  };

  const short
  parser::yydefgoto_[] =
  {
      -1,     2,     3,     4,    77,    13,    90,   143,   189,   190,
     258,   293,   294,    14,    15,   327,   328,    16,    39,    40,
      28,   120,    74,    17,    18,    30,    31,    82,   131,   132,
     133,    19,   107,   108,    20,   205,   243,   244,    21,   148,
      22,    45,    46,   263,   264,   265,   298,   335,   266,   338,
      78,   360,   361,   379,   380,   161,   162,   199,   200,    61,
     231,   269,   270,   168,   233,   275,   276,   235,   280,   281,
     284,   105,    62,    54,   115,   116,   295
  };

  const short
  parser::yytable_[] =
  {
      53,   171,   215,   326,   141,   100,   259,   136,   329,   278,
     330,    26,    84,   110,    79,    29,    32,    35,   331,    26,
     299,     1,    26,   332,    80,    26,   220,    96,    26,    55,
      56,    26,   134,    29,   260,   104,   138,   118,     6,    35,
      73,    42,    43,   144,    29,    47,    48,    49,    50,    57,
      91,    58,    81,   279,   203,   182,   183,   261,   179,   250,
     135,    59,   300,    33,    27,    60,   135,   220,   119,   273,
      29,    29,    52,   153,   154,    63,   262,   163,   289,   165,
      44,   393,    32,   177,   326,     7,    85,    35,   180,   329,
     247,   330,   251,   239,    23,   326,   326,   393,   376,   331,
     329,   329,   330,   330,   332,   274,    26,   197,   255,   376,
     331,   331,   112,   113,   377,   332,   332,   206,   191,   256,
     325,   211,   119,   369,   272,   377,   277,   392,   283,     9,
     325,   221,    36,   222,   384,    96,   201,   370,   401,     9,
      12,    35,   208,   209,   228,   229,   381,   383,    75,   -30,
      12,    41,    26,   156,   157,    64,    65,   303,    73,   388,
     396,    83,   307,   124,    75,    97,    98,  -180,   310,    47,
      48,    49,    50,   314,   145,   158,    37,    38,   163,   111,
     201,   125,   126,   127,   128,   159,    75,    97,    98,   160,
      26,   156,   157,   146,   147,    73,    52,   252,    26,    55,
      56,   253,    24,   191,    86,   130,    25,    47,    48,    49,
      50,   296,   271,   158,   285,    47,    48,    49,    50,   185,
     325,    58,    88,    51,   355,   356,    26,   160,    87,     9,
      89,    59,    97,    98,    52,    60,    47,   186,    49,   187,
      12,    92,    52,    47,    48,    49,    50,   357,    26,   397,
      97,    98,    51,   188,   339,   400,   371,   372,    93,    51,
     198,   255,   318,    52,   285,    47,    48,    49,    50,    94,
      52,    26,   256,   333,   152,   166,    26,   368,   317,   124,
      75,    51,   207,    75,    97,    98,    95,    76,    47,    48,
      49,    50,    52,    47,    48,    49,    50,   125,   126,   127,
     128,   267,   102,   255,    51,    75,   268,   255,   242,    51,
      99,   103,   185,   358,   256,    52,   363,   124,   256,   257,
      52,   130,   255,   382,   364,    47,    48,    49,    50,    47,
     186,    49,   187,   256,     8,   125,   126,   127,   128,   376,
     292,    51,   101,     9,   106,    51,    73,    10,    11,   114,
     129,   255,    52,   390,    12,   377,    52,     8,   117,   130,
      64,    65,   256,   184,   325,   399,     9,     8,   375,   378,
      10,    11,   139,     9,   386,   387,     9,    12,    97,    98,
      10,    11,    97,    98,    12,   121,   223,    12,    97,    98,
     140,    24,   123,   398,    -4,   351,   224,     8,   142,    75,
      97,    98,   376,    75,   137,   155,     9,   109,   218,   219,
      10,    11,   152,   149,   255,   226,   227,    12,   377,    66,
      67,    68,    69,   290,   291,   256,   150,    66,    67,    68,
      69,   151,    70,   164,    71,    72,    73,   169,    65,   167,
     170,  -204,    71,    72,   172,   173,   174,   175,    75,   178,
     192,   181,   193,    98,   212,   194,   195,   196,   202,   214,
     204,   216,   217,   305,   210,   315,   254,   319,   323,   225,
     322,   230,   232,   249,   238,   236,   237,   246,   241,   271,
     301,   234,   282,   308,   286,   287,   288,   297,   302,   306,
     336,   309,   312,   311,   337,   342,   273,   324,   313,   340,
     316,   345,   278,     5,   267,   367,   334,   350,   373,   349,
     352,   344,   348,   354,   359,   365,   366,   374,   353,   385,
     347,   391,   389,   248,   394,   402,    34,   403,   321,   213,
     320,   362,   395,   176,   240,   304,   341,   245,   343,   346,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     0,   122
  };

  const short
  parser::yycheck_[] =
  {
      24,   108,   173,   294,    88,    53,   228,    83,   294,     5,
     294,     3,    36,    61,    18,     9,    10,    11,   294,     3,
       3,    33,     3,   294,    16,     3,   178,    51,     3,     4,
       5,     3,    16,    27,     3,    59,    84,     5,     0,    33,
      44,     7,     8,    91,    38,    20,    21,    22,    23,    24,
      44,    26,    44,    49,   161,   139,   140,    26,   134,     4,
      44,    36,    45,    44,    36,    40,    44,   219,    36,     5,
      64,    65,    47,    97,    98,    27,    45,   101,   249,   103,
      46,   379,    76,   131,   375,     0,    38,    81,   136,   375,
       4,   375,    37,   200,     0,   386,   387,   395,     3,   375,
     386,   387,   386,   387,   375,    41,     3,   155,    15,     3,
     386,   387,    64,    65,    19,   386,   387,   165,   142,    26,
       3,   169,    36,   359,   231,    19,   233,    32,   235,    12,
       3,   179,    35,   181,   370,   159,   160,   359,    32,    12,
      23,   135,   166,   167,   192,   193,   368,   369,    34,    32,
      23,    35,     3,     4,     5,    13,    14,   264,    44,    32,
     382,    16,   269,     3,    34,    13,    14,    37,   275,    20,
      21,    22,    23,   280,     3,    26,    10,    11,   202,    37,
     204,    21,    22,    23,    24,    36,    34,    13,    14,    40,
       3,     4,     5,    22,    23,    44,    47,    37,     3,     4,
       5,   225,    35,   227,    35,    45,    39,    20,    21,    22,
      23,   259,    38,    26,   238,    20,    21,    22,    23,     3,
       3,    26,    31,    36,     3,     4,     3,    40,    35,    12,
       3,    36,    13,    14,    47,    40,    20,    21,    22,    23,
      23,     9,    47,    20,    21,    22,    23,    26,     3,    32,
      13,    14,    36,    37,   302,    36,   363,   364,    36,    36,
      37,    15,   286,    47,   288,    20,    21,    22,    23,    36,
      47,     3,    26,   297,    37,    38,     3,    31,     5,     3,
      34,    36,    37,    34,    13,    14,    36,    38,    20,    21,
      22,    23,    47,    20,    21,    22,    23,    21,    22,    23,
      24,    36,    36,    15,    36,    34,    41,    15,     3,    36,
      39,    34,     3,   337,    26,    47,   340,     3,    26,    31,
      47,    45,    15,    31,   348,    20,    21,    22,    23,    20,
      21,    22,    23,    26,     3,    21,    22,    23,    24,     3,
      33,    36,    40,    12,     5,    36,    44,    16,    17,     4,
      36,    15,    47,   377,    23,    19,    47,     3,     3,    45,
      13,    14,    26,    32,     3,   389,    12,     3,   367,    33,
      16,    17,    31,    12,   373,   374,    12,    23,    13,    14,
      16,    17,    13,    14,    23,     3,    32,    23,    13,    14,
      31,    35,     3,    32,     0,    39,    32,     3,    36,    34,
      13,    14,     3,    34,    39,    26,    12,    38,    37,    38,
      16,    17,    37,     5,    15,    37,    38,    23,    19,    27,
      28,    29,    30,    37,    38,    26,     5,    27,    28,    29,
      30,     5,    40,     5,    42,    43,    44,    41,    14,    38,
      38,    35,    42,    43,    41,    35,     4,    18,    34,    38,
      35,    26,    36,    14,     5,    38,    38,    38,    38,     4,
      38,    38,     3,     5,    37,     3,   227,     3,   292,    39,
       4,    40,    40,    35,    38,    41,    41,    37,    41,    38,
      37,    48,    38,    37,    39,    38,    38,    35,    38,    38,
       3,    38,    35,    37,    25,    41,     5,    32,    38,    38,
      37,     3,     5,     1,    36,    31,    39,    32,    31,    37,
     328,    41,    39,    35,    35,    35,    35,    31,   328,    37,
      49,    32,    39,   213,    32,    32,    11,    37,   288,   172,
     287,   339,   382,   129,   202,   266,   306,   204,   309,   313,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    76
  };

  const signed char
  parser::yystos_[] =
  {
       0,    33,    51,    52,    53,    52,     0,     0,     3,    12,
      16,    17,    23,    55,    63,    64,    67,    73,    74,    81,
      84,    88,    90,     0,    35,    39,     3,    36,    70,   123,
      75,    76,   123,    44,    77,   123,    35,    10,    11,    68,
      69,    35,     7,     8,    46,    91,    92,    20,    21,    22,
      23,    36,    47,   109,   123,     4,     5,    24,    26,    36,
      40,   109,   122,    70,    13,    14,    27,    28,    29,    30,
      40,    42,    43,    44,    72,    34,    38,    54,   100,    18,
      16,    44,    77,    16,   109,    70,    35,    35,    31,     3,
      56,   123,     9,    36,    36,    36,   109,    13,    14,    39,
      54,    40,    36,    34,   109,   121,     5,    82,    83,    38,
      54,    37,    70,    70,     4,   124,   125,     3,     5,    36,
      71,     3,    76,     3,     3,    21,    22,    23,    24,    36,
      45,    78,    79,    80,    16,    44,    78,    39,    54,    31,
      31,    53,    36,    57,    54,     3,    22,    23,    89,     5,
       5,     5,    37,   109,   109,    26,     4,     5,    26,    36,
      40,   105,   106,   109,     5,   109,    38,    38,   113,    41,
      38,   113,    41,    35,     4,    18,    79,    54,    38,    78,
      54,    26,    53,    53,    32,     3,    21,    23,    37,    58,
      59,   109,    35,    36,    38,    38,    38,    54,    37,   107,
     108,   109,    38,   113,    38,    85,    54,    37,   109,   109,
      37,    54,     5,    72,     4,   125,    38,     3,    37,    38,
      80,    54,    54,    32,    32,    39,    37,    38,    54,    54,
      40,   110,    40,   114,    48,   117,    41,    41,    38,   113,
     106,    41,     3,    86,    87,   108,    37,     4,    71,    35,
       4,    37,    37,   109,    59,    15,    26,    31,    60,   126,
       3,    26,    45,    93,    94,    95,    98,    36,    41,   111,
     112,    38,   113,     5,    41,   115,   116,   113,     5,    49,
     118,   119,    38,   113,   120,   109,    39,    38,    38,   125,
      37,    38,    33,    61,    62,   126,    54,    35,    96,     3,
      45,    37,    38,   113,    96,     5,    38,   113,    37,    38,
     113,    37,    35,    38,   113,     3,    37,     5,   109,     3,
      87,    86,     4,    61,    32,     3,    55,    65,    66,    67,
      73,    81,    88,   109,    39,    97,     3,    25,    99,    54,
      38,   112,    41,   116,    41,     3,   119,    49,    39,    37,
      32,    39,    68,    69,    35,     3,     4,    26,   109,    35,
     101,   102,    95,   109,   109,    35,    35,    31,    31,   100,
     126,   113,   113,    31,    31,    62,     3,    19,    33,   103,
     104,   126,    31,   126,   100,    37,    62,    62,    32,    39,
     109,    32,    32,   104,    32,   103,   126,    32,    32,   109,
      36,    32,    32,    37
  };

  const signed char
  parser::yyr1_[] =
  {
       0,    50,    51,    51,    52,    53,    53,    53,    53,    53,
      53,    53,    53,    54,    54,    55,    56,    57,    57,    57,
      58,    58,    59,    59,    59,    59,    60,    60,    60,    61,
      61,    62,    62,    62,    62,    62,    62,    63,    63,    64,
      64,    65,    65,    66,    66,    67,    68,    69,    70,    70,
      70,    70,    70,    70,    70,    71,    71,    71,    72,    72,
      72,    72,    72,    72,    73,    73,    73,    73,    73,    73,
      73,    73,    73,    74,    74,    74,    74,    75,    75,    76,
      76,    77,    77,    78,    78,    78,    79,    79,    80,    80,
      80,    80,    80,    80,    80,    81,    81,    82,    82,    83,
      83,    84,    85,    85,    85,    85,    86,    86,    87,    87,
      88,    89,    89,    89,    90,    90,    91,    92,    92,    93,
      93,    94,    94,    95,    95,    95,    95,    96,    96,    97,
      97,    97,    97,    98,    98,    99,    99,   100,   101,   101,
     101,   102,   102,   102,   102,   102,   102,   102,   103,   103,
     104,   104,   104,   105,   105,   106,   106,   106,   106,   106,
     107,   107,   108,   108,   109,   109,   109,   109,   109,   109,
     109,   109,   109,   109,   109,   110,   110,   111,   111,   112,
     113,   113,   114,   114,   115,   115,   116,   117,   117,   118,
     118,   119,   120,   120,   121,   121,   122,   122,   122,   123,
     123,   124,   124,   124,   125,   125,   126,   126
  };

  const signed char
  parser::yyr2_[] =
  {
       0,     2,     2,     3,     1,     2,     2,     2,     2,     2,
       2,     2,     0,     1,     0,     7,     1,     3,     2,     0,
       3,     1,     1,     3,     1,     1,     2,     3,     4,     1,
       1,     2,     2,     2,     2,     2,     0,     6,     1,     5,
       6,     6,     1,     5,     6,     2,     2,     1,     3,     3,
       6,     6,     3,     3,     3,     4,     5,     7,     1,     1,
       1,     1,     1,     1,     3,     3,     3,     3,     6,     4,
       6,     4,     6,     3,     5,     5,     6,     3,     1,     1,
       3,     1,     2,     1,     3,     4,     3,     1,     1,     1,
       1,     1,     1,     1,     3,     4,     6,     2,     0,     3,
       1,     7,     0,     2,     2,     4,     3,     1,     3,     3,
      10,     1,     1,     1,     2,     0,     3,     1,     0,     2,
       0,     4,     1,     3,     1,     2,     1,     2,     0,     2,
       2,     2,     0,     2,     3,     2,     0,     2,     5,     4,
       1,     2,     3,     3,     5,     4,     4,     0,     2,     1,
       3,     2,     4,     3,     1,     1,     1,     1,     1,     3,
       2,     0,     3,     1,     1,     5,     5,     7,     7,     7,
       3,     3,     3,     1,     1,     4,     2,     3,     1,     6,
       1,     0,     4,     2,     3,     1,     1,     4,     2,     3,
       1,     3,     5,     1,     3,     3,     4,     4,     2,     1,
       3,     1,     3,     5,     1,     0,     1,     1
  };


#if PYTYPEDEBUG || 1
  // YYTNAME[SYMBOL-NUM] -- String name of the symbol SYMBOL-NUM.
  // First, the terminals, then, starting at \a YYNTOKENS, nonterminals.
  const char*
  const parser::yytname_[] =
  {
  "\"end of file\"", "error", "\"invalid token\"", "NAME", "NUMBER",
  "STRING", "LEXERROR", "ASYNC", "CLASS", "DEF", "ELSE", "ELIF", "IF",
  "OR", "AND", "PASS", "IMPORT", "FROM", "AS", "RAISE", "NOTHING",
  "NAMEDTUPLE", "COLL_NAMEDTUPLE", "TYPEDDICT", "TYPEVAR", "ARROW",
  "ELLIPSIS", "EQ", "NE", "LE", "GE", "INDENT", "DEDENT", "TRIPLEQUOTED",
  "TYPECOMMENT", "':'", "'('", "')'", "','", "'='", "'['", "']'", "'<'",
  "'>'", "'.'", "'*'", "'@'", "'?'", "'{'", "'}'", "$accept", "start",
  "unit", "alldefs", "maybe_type_ignore", "classdef", "class_name",
  "parents", "parent_list", "parent", "maybe_class_funcs", "class_funcs",
  "funcdefs", "if_stmt", "if_and_elifs", "class_if_stmt",
  "class_if_and_elifs", "if_cond", "elif_cond", "else_cond", "condition",
  "version_tuple", "condition_op", "constantdef", "importdef",
  "import_items", "import_item", "import_name", "from_list", "from_items",
  "from_item", "alias_or_constant", "maybe_string_list", "string_list",
  "typevardef", "typevar_args", "typevar_kwargs", "typevar_kwarg",
  "funcdef", "funcname", "decorators", "decorator", "maybe_async",
  "params", "param_list", "param", "param_type", "param_default",
  "param_star_name", "return", "typeignore", "maybe_body", "empty_body",
  "body", "body_stmt", "type_parameters", "type_parameter",
  "maybe_type_list", "type_list", "type", "named_tuple_fields",
  "named_tuple_field_list", "named_tuple_field", "maybe_comma",
  "coll_named_tuple_fields", "coll_named_tuple_field_list",
  "coll_named_tuple_field", "typed_dict_fields", "typed_dict_field_dict",
  "typed_dict_field", "maybe_typed_dict_kwarg", "type_tuple_elements",
  "type_tuple_literal", "dotted_name", "getitem_key", "maybe_number",
  "pass_or_ellipsis", YY_NULLPTR
  };
#endif


#if PYTYPEDEBUG
  const short
  parser::yyrline_[] =
  {
       0,   135,   135,   136,   140,   144,   145,   146,   147,   153,
     154,   155,   160,   164,   165,   172,   182,   193,   194,   195,
     199,   200,   204,   205,   206,   207,   214,   215,   216,   220,
     221,   225,   226,   231,   232,   237,   238,   243,   246,   251,
     255,   268,   271,   276,   280,   292,   296,   300,   304,   307,
     310,   313,   316,   317,   318,   322,   323,   324,   330,   331,
     332,   333,   334,   335,   339,   343,   347,   351,   355,   359,
     363,   367,   371,   378,   382,   386,   392,   401,   402,   406,
     407,   412,   413,   420,   421,   422,   426,   427,   431,   432,
     435,   438,   441,   444,   447,   451,   452,   456,   457,   461,
     462,   466,   473,   474,   475,   476,   480,   481,   485,   487,
     491,   505,   506,   507,   511,   512,   516,   520,   521,   525,
     526,   538,   539,   543,   544,   545,   546,   550,   551,   555,
     556,   557,   558,   562,   563,   567,   568,   572,   576,   577,
     578,   582,   583,   584,   585,   586,   587,   588,   592,   593,
     597,   598,   599,   603,   604,   608,   609,   611,   612,   614,
     621,   622,   626,   627,   631,   635,   639,   643,   647,   651,
     655,   656,   657,   658,   659,   663,   664,   668,   669,   673,
     677,   678,   682,   683,   687,   690,   694,   698,   699,   703,
     708,   712,   716,   717,   724,   725,   734,   739,   745,   752,
     753,   767,   768,   773,   781,   782,   786,   787
  };

  void
  parser::yy_stack_print_ () const
  {
    *yycdebug_ << "Stack now";
    for (stack_type::const_iterator
           i = yystack_.begin (),
           i_end = yystack_.end ();
         i != i_end; ++i)
      *yycdebug_ << ' ' << int (i->state);
    *yycdebug_ << '\n';
  }

  void
  parser::yy_reduce_print_ (int yyrule) const
  {
    int yylno = yyrline_[yyrule];
    int yynrhs = yyr2_[yyrule];
    // Print the symbols being reduced, and their result.
    *yycdebug_ << "Reducing stack by rule " << yyrule - 1
               << " (line " << yylno << "):\n";
    // The symbols being reduced.
    for (int yyi = 0; yyi < yynrhs; yyi++)
      YY_SYMBOL_PRINT ("   $" << yyi + 1 << " =",
                       yystack_[(yynrhs) - (yyi + 1)]);
  }
#endif // PYTYPEDEBUG

  parser::symbol_kind_type
  parser::yytranslate_ (int t)
  {
    // YYTRANSLATE[TOKEN-NUM] -- Symbol number corresponding to
    // TOKEN-NUM as returned by yylex.
    static
    const signed char
    translate_table[] =
    {
       0,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
      36,    37,    45,     2,    38,     2,    44,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,    35,     2,
      42,    39,    43,    47,    46,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,    40,     2,    41,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,    48,     2,    49,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     1,     2,     3,     4,
       5,     6,     7,     8,     9,    10,    11,    12,    13,    14,
      15,    16,    17,    18,    19,    20,    21,    22,    23,    24,
      25,    26,    27,    28,    29,    30,    31,    32,    33,    34
    };
    const int user_token_number_max_ = 289;

    if (t <= 0)
      return symbol_kind::S_YYEOF;
    else if (t <= user_token_number_max_)
      return YY_CAST (symbol_kind_type, translate_table[t]);
    else
      return symbol_kind::S_YYUNDEF;
  }

#line 17 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
} // pytype
#line 3254 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"

#line 790 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"


void pytype::parser::error(const location& loc, const std::string& msg) {
  ctx->SetErrorLocation(loc);
  pytype::Lexer* lexer = pytypeget_extra(scanner);
  if (lexer->error_message_) {
    PyErr_SetObject(ctx->Value(pytype::kParseError), lexer->error_message_);
  } else {
    PyErr_SetString(ctx->Value(pytype::kParseError), msg.c_str());
  }
}

namespace {

PyObject* StartList(PyObject* item) {
  return Py_BuildValue("[N]", item);
}

PyObject* AppendList(PyObject* list, PyObject* item) {
  PyList_Append(list, item);
  Py_DECREF(item);
  return list;
}

PyObject* ExtendList(PyObject* dst, PyObject* src) {
  // Add items from src to dst (both of which must be lists) and return src.
  // Borrows the reference to src.
  Py_ssize_t count = PyList_Size(src);
  for (Py_ssize_t i=0; i < count; ++i) {
    PyList_Append(dst, PyList_GetItem(src, i));
  }
  Py_DECREF(src);
  return dst;
}

}  // end namespace

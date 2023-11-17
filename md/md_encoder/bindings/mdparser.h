#ifndef __MDPARSER_H__
#define __MDPARSER_H__

#include <stdint.h>

typedef struct CProto
{
    const uint8_t *data;
    uint32_t len;
} CProto;

typedef struct CProtoVec
{
    const CProto **data;
    uint32_t len;
} CProtoVec;

typedef struct CProtoGenerator
{
    void *ctx;
} CProtoGenerator;

CProtoGenerator *(*init_proto_generator)(uint32_t parallel_threshold);
void (*set_threshold)(CProtoGenerator *ptr, uint32_t parallel_threshold);
uint32_t (*get_threshold)(CProtoGenerator *ptr);
const CProtoVec *(*generate_proto)(CProtoGenerator *ptr,
                                   char *input);
void (*free_proto)(const CProto *ptr);
void (*free_proto_vec)(const CProtoVec *ptr);

#endif
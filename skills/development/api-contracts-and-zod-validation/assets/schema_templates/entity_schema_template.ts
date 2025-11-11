import { z } from 'zod';

/**
 * Entity validation schema template for worldbuilding applications
 *
 * Common schemas for worldbuilding entities like characters, locations, items, etc.
 */

// Base entity schema (shared fields across all entities)
const baseEntitySchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1, 'Name is required').max(200),
  description: z.string().max(5000).optional(),
  tags: z.array(z.string()).max(20),
  metadata: z.object({
    createdAt: z.date(),
    updatedAt: z.date(),
    createdBy: z.string(),
  }),
});

// Entity types enum
export const entityTypeSchema = z.enum([
  'character',
  'location',
  'item',
  'faction',
  'event',
  'concept',
]);

export type EntityType = z.infer<typeof entityTypeSchema>;

// Character entity schema
export const characterSchema = baseEntitySchema.extend({
  type: z.literal('character'),
  attributes: z.object({
    age: z.number().int().nonnegative().optional(),
    gender: z.string().optional(),
    species: z.string().optional(),
    occupation: z.string().optional(),
    birthplace: z.string().uuid().optional(), // Reference to location entity
  }),
  relationships: z.array(
    z.object({
      targetId: z.string().uuid(),
      type: z.string(),
      strength: z.number().min(0).max(1).optional(),
    })
  ),
});

export type Character = z.infer<typeof characterSchema>;

// Location entity schema
export const locationSchema = baseEntitySchema.extend({
  type: z.literal('location'),
  attributes: z.object({
    locationType: z.enum(['city', 'region', 'country', 'landmark', 'building', 'other']),
    population: z.number().int().nonnegative().optional(),
    parentLocation: z.string().uuid().optional(), // Reference to parent location
    coordinates: z.object({
      x: z.number(),
      y: z.number(),
    }).optional(),
  }),
});

export type Location = z.infer<typeof locationSchema>;

// Item entity schema
export const itemSchema = baseEntitySchema.extend({
  type: z.literal('item'),
  attributes: z.object({
    itemType: z.enum(['weapon', 'armor', 'tool', 'artifact', 'consumable', 'other']),
    rarity: z.enum(['common', 'uncommon', 'rare', 'legendary']).optional(),
    owner: z.string().uuid().optional(), // Reference to character entity
    location: z.string().uuid().optional(), // Reference to location entity
  }),
});

export type Item = z.infer<typeof itemSchema>;

// Faction/Organization entity schema
export const factionSchema = baseEntitySchema.extend({
  type: z.literal('faction'),
  attributes: z.object({
    factionType: z.enum(['guild', 'government', 'religion', 'military', 'criminal', 'other']),
    size: z.enum(['small', 'medium', 'large', 'massive']).optional(),
    headquarters: z.string().uuid().optional(), // Reference to location entity
    leader: z.string().uuid().optional(), // Reference to character entity
    founded: z.object({
      year: z.number().int(),
      month: z.number().int().min(1).max(12).optional(),
      day: z.number().int().min(1).max(31).optional(),
    }).optional(),
  }),
  members: z.array(
    z.object({
      characterId: z.string().uuid(),
      role: z.string(),
      joinDate: z.date().optional(),
    })
  ),
});

export type Faction = z.infer<typeof factionSchema>;

// Event entity schema
export const eventSchema = baseEntitySchema.extend({
  type: z.literal('event'),
  attributes: z.object({
    eventType: z.enum(['battle', 'meeting', 'ceremony', 'discovery', 'disaster', 'other']),
    date: z.object({
      year: z.number().int(),
      month: z.number().int().min(1).max(12).optional(),
      day: z.number().int().min(1).max(31).optional(),
    }),
    location: z.string().uuid().optional(), // Reference to location entity
    participants: z.array(z.string().uuid()), // References to character entities
  }),
}).refine(
  (data) => !data.attributes.date.day || data.attributes.date.month,
  { message: 'Month is required when day is specified', path: ['attributes', 'date', 'month'] }
);

export type Event = z.infer<typeof eventSchema>;

// Concept entity schema (abstract ideas, magic systems, technologies, etc.)
export const conceptSchema = baseEntitySchema.extend({
  type: z.literal('concept'),
  attributes: z.object({
    conceptType: z.enum(['magic', 'technology', 'philosophy', 'language', 'custom']),
    relatedEntities: z.array(z.string().uuid()), // References to any entity
  }),
});

export type Concept = z.infer<typeof conceptSchema>;

// Union of all entity types
export const entitySchema = z.discriminatedUnion('type', [
  characterSchema,
  locationSchema,
  itemSchema,
  factionSchema,
  eventSchema,
  conceptSchema,
]);

export type Entity = z.infer<typeof entitySchema>;

// Relationship schema
export const relationshipSchema = z.object({
  id: z.string().uuid(),
  sourceId: z.string().uuid(),
  targetId: z.string().uuid(),
  type: z.string().min(1).max(50),
  description: z.string().max(500).optional(),
  strength: z.number().min(0).max(1).optional(),
  metadata: z.record(z.string(), z.any()).optional(),
  createdAt: z.date(),
  updatedAt: z.date(),
}).refine(
  (data) => data.sourceId !== data.targetId,
  { message: 'Source and target must be different entities', path: ['targetId'] }
);

export type Relationship = z.infer<typeof relationshipSchema>;

// Create entity input schema (without auto-generated fields)
export const createEntityInputSchema = z.object({
  type: entityTypeSchema,
  name: z.string().min(1).max(200),
  description: z.string().max(5000).optional(),
  tags: z.array(z.string()).max(20).default([]),
  attributes: z.record(z.string(), z.any()),
});

export type CreateEntityInput = z.infer<typeof createEntityInputSchema>;

// Update entity input schema (partial)
export const updateEntityInputSchema = z.object({
  name: z.string().min(1).max(200).optional(),
  description: z.string().max(5000).optional(),
  tags: z.array(z.string()).max(20).optional(),
  attributes: z.record(z.string(), z.any()).optional(),
}).refine(
  (data) => Object.keys(data).length > 0,
  { message: 'At least one field must be provided for update' }
);

export type UpdateEntityInput = z.infer<typeof updateEntityInputSchema>;

// Query/filter schema for entity search
export const entityQuerySchema = z.object({
  query: z.string().optional(),
  types: z.array(entityTypeSchema).optional(),
  tags: z.array(z.string()).optional(),
  createdAfter: z.date().optional(),
  createdBefore: z.date().optional(),
  createdBy: z.string().optional(),
  pagination: z.object({
    page: z.number().int().positive().default(1),
    limit: z.number().int().min(1).max(100).default(10),
  }).optional(),
  sortBy: z.enum(['name', 'createdAt', 'updatedAt']).default('createdAt'),
  sortOrder: z.enum(['asc', 'desc']).default('desc'),
});

export type EntityQuery = z.infer<typeof entityQuerySchema>;

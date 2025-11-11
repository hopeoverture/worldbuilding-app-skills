import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function main() {
  console.log('🌱 Starting seed...');

  // Create or update settings (singleton)
  const settings = await prisma.settings.upsert({
    where: { id: '00000000-0000-0000-0000-000000000001' },
    update: {},
    create: {
      id: '00000000-0000-0000-0000-000000000001',
      siteName: 'My Worldbuilding App',
      siteUrl: 'https://example.com',
      description: 'A platform for building immersive worlds',
      metaTitle: 'Worldbuilding App - Create Amazing Worlds',
      metaDescription: 'Build, manage, and share your fictional worlds',
      enableComments: true,
      enableRegistration: true,
      maintenanceMode: false,
    },
  });

  console.log('[OK] Settings created:', settings.siteName);

  // Create sample tags
  const tags = await Promise.all([
    prisma.tag.upsert({
      where: { slug: 'worldbuilding' },
      update: {},
      create: {
        name: 'Worldbuilding',
        slug: 'worldbuilding',
      },
    }),
    prisma.tag.upsert({
      where: { slug: 'character-development' },
      update: {},
      create: {
        name: 'Character Development',
        slug: 'character-development',
      },
    }),
    prisma.tag.upsert({
      where: { slug: 'lore' },
      update: {},
      create: {
        name: 'Lore',
        slug: 'lore',
      },
    }),
  ]);

  console.log(`[OK] Created ${tags.length} tags`);

  // Create sample user profile (only if doesn't exist)
  const sampleUser = await prisma.profile.upsert({
    where: { email: 'demo@example.com' },
    update: {},
    create: {
      id: '00000000-0000-0000-0000-000000000002',
      email: 'demo@example.com',
      name: 'Demo User',
      bio: 'Sample user for testing',
      role: 'USER',
    },
  });

  console.log('[OK] Sample user created:', sampleUser.email);

  // Create sample post
  const samplePost = await prisma.post.upsert({
    where: { slug: 'getting-started-with-worldbuilding' },
    update: {},
    create: {
      title: 'Getting Started with Worldbuilding',
      slug: 'getting-started-with-worldbuilding',
      excerpt: 'Learn the basics of creating your own fictional world',
      content: `
# Getting Started with Worldbuilding

Worldbuilding is the process of constructing an imaginary world, sometimes associated with a whole fictional universe.

## Key Elements

1. **Geography**: Define the physical layout of your world
2. **History**: Create a timeline of major events
3. **Culture**: Develop societies and their customs
4. **Magic/Technology**: Establish the rules of your world

Start small and expand gradually. You don't need to build everything at once!
      `.trim(),
      published: true,
      publishedAt: new Date(),
      authorId: sampleUser.id,
    },
  });

  console.log('[OK] Sample post created:', samplePost.title);

  // Link tags to post
  await prisma.postTag.upsert({
    where: {
      postId_tagId: {
        postId: samplePost.id,
        tagId: tags[0].id,
      },
    },
    update: {},
    create: {
      postId: samplePost.id,
      tagId: tags[0].id,
    },
  });

  await prisma.postTag.upsert({
    where: {
      postId_tagId: {
        postId: samplePost.id,
        tagId: tags[2].id,
      },
    },
    update: {},
    create: {
      postId: samplePost.id,
      tagId: tags[2].id,
    },
  });

  console.log('[OK] Tags linked to post');

  // Create sample comment
  await prisma.comment.upsert({
    where: { id: '00000000-0000-0000-0000-000000000003' },
    update: {},
    create: {
      id: '00000000-0000-0000-0000-000000000003',
      content: 'Great introduction! Looking forward to more posts.',
      postId: samplePost.id,
      authorId: sampleUser.id,
    },
  });

  console.log('[OK] Sample comment created');

  console.log('🎉 Seed completed successfully!');
}

main()
  .then(async () => {
    await prisma.$disconnect();
  })
  .catch(async (e) => {
    console.error('[ERROR] Seed failed:', e);
    await prisma.$disconnect();
    process.exit(1);
  });
